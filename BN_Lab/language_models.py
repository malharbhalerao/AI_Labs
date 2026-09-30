import random
from collections import defaultdict

# --- Dataset Preparation ---
raw_data = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug"
]

def preprocess(data):
    """Tokenizes and adds <START> and <END> tags."""
    return [["<START>"] + sentence.lower().split() + ["<END>"] for sentence in data]

dataset = preprocess(raw_data)

# --- First-Order Autoregressive Model ---
class FirstOrderMarkovLM:
    def __init__(self):
        self.counts = defaultdict(lambda: defaultdict(int))
        self.cpt = defaultdict(dict)

    def train(self, data):
        # Count transitions
        for sentence in data:
            for i in range(len(sentence) - 1):
                current_word = sentence[i]
                next_word = sentence[i+1]
                self.counts[current_word][next_word] += 1
                
        # Construct Conditional Probability Table (CPT)
        for current_word, transitions in self.counts.items():
            total = sum(transitions.values())
            for next_word, count in transitions.items():
                self.cpt[current_word][next_word] = count / total

    def test_normalization(self):
        """Tests that probabilities sum to 1.0 for each context."""
        results = {}
        for word in self.cpt:
            total = sum(self.cpt[word].values())
            results[word] = total
            print(f"Normalization test for '{word}': {total:.4f}")
        return results

    def predict_greedy(self, current_word):
        if current_word not in self.cpt:
            return "<END>"
        # Return the word with the max probability
        return max(self.cpt[current_word], key=self.cpt[current_word].get)

    def predict_sample(self, current_word):
        if current_word not in self.cpt:
            return "<END>"
        choices = list(self.cpt[current_word].keys())
        probabilities = list(self.cpt[current_word].values())
        return random.choices(choices, weights=probabilities, k=1)[0]

    def generate_sentence(self, mode="sample"):
        sentence = []
        current_word = "<START>"
        while True:
            if mode == "greedy":
                next_word = self.predict_greedy(current_word)
            else:
                next_word = self.predict_sample(current_word)
                
            if next_word == "<END>":
                break
            sentence.append(next_word)
            current_word = next_word
        return " ".join(sentence)


# --- Second-Order Autoregressive Model ---
class SecondOrderMarkovLM:
    def __init__(self):
        self.counts = defaultdict(lambda: defaultdict(int))
        self.cpt = defaultdict(dict)

    def train(self, data):
        for sentence in data:
            # Need at least <START> <START> to predict the first real word if using strict trigrams,
            # but we can pad the start with two tokens.
            padded = ["<START>", "<START>"] + sentence[1:] 
            for i in range(len(padded) - 2):
                context = (padded[i], padded[i+1])
                next_word = padded[i+2]
                self.counts[context][next_word] += 1
                
        for context, transitions in self.counts.items():
            total = sum(transitions.values())
            for next_word, count in transitions.items():
                self.cpt[context][next_word] = count / total

    def predict_sample(self, context):
        if context not in self.cpt:
            return "<END>"
        choices = list(self.cpt[context].keys())
        probabilities = list(self.cpt[context].values())
        return random.choices(choices, weights=probabilities, k=1)[0]

    def generate_sentence(self):
        sentence = []
        context = ("<START>", "<START>")
        # Prime the first word based on the dataset structure
        if context not in self.cpt:
             context = ("<START>", "the")
             sentence.append("the")
             
        while True:
            next_word = self.predict_sample(context)
            if next_word == "<END>":
                break
            sentence.append(next_word)
            context = (context[1], next_word)
        return " ".join(sentence)

# --- Execution ---
if __name__ == "__main__":
    print("--- First Order Model ---")
    lm1 = FirstOrderMarkovLM()
    lm1.train(dataset)
    lm1.test_normalization()
    
    print("\nGenerated (Greedy):")
    for _ in range(3): print(lm1.generate_sentence(mode="greedy"))
    
    print("\nGenerated (Sample):")
    for _ in range(3): print(lm1.generate_sentence(mode="sample"))
