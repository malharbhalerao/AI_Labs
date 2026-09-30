import torch
import torch.nn as nn
import torch.optim as optim
import math

# Task 1: Dataset Setup
# X1 | X2 | Y
X = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
Y_binary = torch.tensor([[0.0], [1.0], [1.0], [0.0]])
Y_multiclass = torch.tensor([0, 1, 1, 2]) # 0: both inactive, 1: disagree, 2: both active

class XORModel(nn.Module):
    def __init__(self, hidden_activation, out_features=1):
        super().__init__()
        self.hidden = nn.Linear(2, 2)
        self.act = hidden_activation
        self.out = nn.Linear(2, out_features)

    def forward(self, x):
        h = self.act(self.hidden(x))
        return self.out(h)

def train_model(model, X, Y, criterion, epochs=2500, lr=0.1, record_early_grad=False):
    optimizer = optim.SGD(model.parameters(), lr=lr)
    early_grad_norm = None

    for epoch in range(epochs):
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, Y)
        loss.backward()
        
        if record_early_grad and epoch == 5:
            # Calculate Euclidean norm of the first layer gradient
            early_grad_norm = torch.norm(model.hidden.weight.grad).item()
            
        optimizer.step()
        
    return loss.item(), early_grad_norm

# --- Task 4A & 4B: Basic Learning & Backprop Check ---
def run_basic_binary():
    print("--- Task 4A & 4B: Basic Binary XOR (Tanh) ---")
    torch.manual_seed(42)
    model = XORModel(nn.Tanh(), out_features=1)
    criterion = nn.BCEWithLogitsLoss()
    
    initial_loss = criterion(model(X), Y_binary).item()
    train_model(model, X, Y_binary, criterion)
    
    with torch.no_grad():
        logits = model(X)
        probs = torch.sigmoid(logits)
        preds = (probs >= 0.5).float()
    
    print(f"Initial Loss: {initial_loss:.4f} | Final Loss: {criterion(logits, Y_binary).item():.4f}")
    print("Probs:\n", probs.squeeze().numpy())
    print("Preds:\n", preds.squeeze().numpy())
    
    # Backprop check (one backward pass to inspect grad)
    model.zero_grad()
    criterion(model(X), Y_binary).backward()
    print("W(1) Gradients:\n", model.hidden.weight.grad.numpy())
    print("\n")

# --- Task 4C: Symmetry Experiment ---
def run_symmetry_experiment():
    print("--- Task 4C: Zero-Initialization Symmetry ---")
    model = XORModel(nn.Tanh(), out_features=1)
    # Force weights to zero
    nn.init.zeros_(model.hidden.weight)
    nn.init.zeros_(model.hidden.bias)
    nn.init.zeros_(model.out.weight)
    nn.init.zeros_(model.out.bias)
    
    train_model(model, X, Y_binary, nn.BCEWithLogitsLoss(), epochs=100)
    print("W(1) weights after 100 steps (Notice identical rows):")
    print(model.hidden.weight.detach().numpy())
    print("\n")

# --- Task 4D: Activation Experiment ---
def run_activation_experiment():
    print("--- Task 4D: Activation Comparison ---")
    activations = [("Sigmoid", nn.Sigmoid()), ("Tanh", nn.Tanh()), ("ReLU", nn.ReLU())]
    criterion = nn.BCEWithLogitsLoss()
    
    for name, act in activations:
        torch.manual_seed(42) # Consistent seed for fair comparison
        model = XORModel(act, out_features=1)
        final_loss, grad_norm = train_model(model, X, Y_binary, criterion, record_early_grad=True)
        
        with torch.no_grad():
            preds = (torch.sigmoid(model(X)) >= 0.5).float()
            correct = (preds == Y_binary).all().item()
            
        print(f"{name:8} | Loss: {final_loss:.4f} | 4/4 Correct: {correct} | Early Grad Norm: {grad_norm:.4f}")
    print("\n")

# --- Task 5: 3-Class Extension ---
def run_multiclass():
    print("--- Task 5: 3-Class Extension ---")
    torch.manual_seed(42)
    model = XORModel(nn.Tanh(), out_features=3)
    criterion = nn.CrossEntropyLoss()
    
    train_model(model, X, Y_multiclass, criterion, lr=0.5)
    
    with torch.no_grad():
        logits = model(X)
        probs = torch.softmax(logits, dim=1)
        preds = torch.argmax(probs, dim=1)
        
    print("Final Probs:\n", probs.numpy())
    print("Predicted Classes:", preds.numpy())
    print(f"Probabilities sum to 1? {torch.allclose(probs.sum(dim=1), torch.ones(4))}")
    
    # Optional Diagnostic: Add 100 to logits
    test_idx = 1
    original_logit = logits[test_idx]
    shifted_logit = original_logit + 100.0
    shifted_prob = torch.softmax(shifted_logit.unsqueeze(0), dim=1)
    
    print(f"\nOriginal Softmax for {X[test_idx].numpy()}: {probs[test_idx].numpy()}")
    print(f"Shifted (+100) Softmax: {shifted_prob.squeeze().numpy()}")

if __name__ == "__main__":
    run_basic_binary()
    run_symmetry_experiment()
    run_activation_experiment()
    run_multiclass()
