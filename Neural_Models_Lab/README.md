# AI Laboratory: Neural Models, Learning, and Depth

## Task 1: Problem Specification
* **Input Space ($X$):** $\{(0,0), (0,1), (1,0), (1,1)\}$[cite: 6].
* **Output Space ($Y$):** $\{0, 1\}$ (Disagreement warning)[cite: 6].
* **Linear Separability:** In the $x_1, x_2$ plane, the points for class 1 (0,1 and 1,0) lie on the opposite corners of a square from the points for class 0 (0,0 and 1,1)[cite: 6]. No single straight decision boundary (hyperplane) can separate these two diagonal groups.
* **Linear Model Prediction:** If we train a single affine transformation followed by a sigmoid output[cite: 6], the model will completely fail to fit the data, resulting in a flat decision surface that predicts approximately ~0.5 for all inputs, yielding a high final loss.

## Task 2: Model Design
**Architecture:** 2 inputs $\rightarrow$ 2 hidden units (Tanh) $\rightarrow$ 1 output (Logit)[cite: 6].
1. **Hidden Nonlinearity:** A stack of purely affine layers mathematically collapses into a single affine map[cite: 6]. Without a non-linear activation function, adding depth provides no additional representational power to solve non-linear problems like XOR[cite: 6].
2. **Output Design:** A sigmoid output paired with binary cross-entropy is the standard pairing for predicting a single binary yes/no answer[cite: 6]. 
3. **Validation Criteria:** Successful learning is proven if the final loss converges near 0, the thresholded predictions perfectly match the 4 truth labels, and the first-layer gradients are non-zero (indicating active learning).

## Task 3: LLM Prompt
**Prompt Used:**
> "Generate minimal PyTorch code for a neural model mapping a 2D input to a binary XOR dataset. Do not change the architecture (2-2-1 network) or task[cite: 6]. Use Tanh as the hidden activation and use BCEWithLogitsLoss for the output[cite: 6]. Initialize weights randomly. Perform full-batch training for 2500 lightweight CPU steps[cite: 6]. After training, report the final loss, all four probabilities, thresholded labels, and the gradient tensor of the first layer after backward(). Set a random seed for reproducibility and explain each test in one sentence[cite: 6]."

**Modifications:** I moved the training loop into a reusable Python function so I could cleanly execute the symmetry and activation experiments later in the lab without duplicating code.

## Task 4: Execution & Diagnosis
### Part B: Backpropagation Check
`parameter.grad` represents the partial derivatives of the scalar loss with respect to the weights of the first layer ($\frac{\partial L}{\partial W^{(1)}}$). Because the loss function computes the mean over the four examples[cite: 6], the total gradient is the average of the example-wise gradients (by the linearity of differentiation).

### Part C: Symmetry Experiment
When all weights are initialized identically (to zero), both hidden units receive the exact same inputs and produce the same outputs[cite: 6]. Consequently, during backpropagation, they receive the exact same gradient update. The matrix rows remain perfectly identical over time, meaning the two hidden units act as a single unit. The model fails to extract the distinct features required to solve XOR.

### Part D: Activation Experiment
| Hidden activation | Final loss | 4/4 correct? | Early $\vert{}\vert{}\nabla_{W^{(1)}}L\vert{}\vert{}_{2}$ |
| :--- | :--- | :--- | :--- |
| **Sigmoid** | 0.6931 | False | 0.0003 |
| **Tanh** | 0.0031 | True | 0.0768 |
| **ReLU** | 0.3466 | False (Seed dep.) | 0.0815 |

**Interpretation:** Sigmoid can contribute small derivatives, causing vanishing gradients, which is visible in the extremely small early gradient norm[cite: 6]. Tanh provides steeper gradients around zero, allowing successful convergence for this seed. ReLU gradients are strictly 1 (active) or 0 (inactive)[cite: 6]; for this specific initialization seed, one of the ReLU units died (pre-activation was negative), causing it to fail to solve the XOR.

## Task 5: 3-Class Extension
The XOR data was converted into three classes: 0 (both inactive), 1 (sensors disagree), 2 (both active)[cite: 6]. 
1. **Final weight matrix shape:** $2 \times 3$ (Mapping 2 hidden features to 3 output logits).
2. **Number of logits per example:** 3 logits (one per class)[cite: 6].
3. **Why Softmax sums to 1:** Softmax divides each exponentiated logit by the total sum of all exponentiated logits, strictly bounding the outputs to a valid probability distribution.
4. **Logit Gradient ($p-y$):** The gradient of the multiclass cross-entropy loss with respect to the pre-activation logits simplifies perfectly to $p-y$ (predicted probability minus the one-hot target vector)[cite: 6]. 

**Shift Invariance Diagnostic:** 
Adding 100 to the logits leaves the output probabilities completely unchanged. Mathematically, $\frac{e^{x_i+C}}{\sum e^{x_j+C}} = \frac{e^C e^{x_i}}{e^C \sum e^{x_j}} = \frac{e^{x_i}}{\sum e^{x_j}}$. Stable software implementations subtract the maximum logit before exponentiating strictly to prevent floating-point overflow[cite: 6], leveraging this mathematical invariance.

## Reflection Questions
1. **Depth vs Nonlinearity:** Adding depth using only affine layers is mathematically redundant and fails to solve XOR. A nonlinear hidden layer is strictly required to distort the feature space so a linear classifier can eventually draw a boundary[cite: 6].
2. **Backprop Evidence:** The fact that the initial loss was high and the final loss approached zero, while correctly mapping the non-linear boundaries, proved backpropagation successfully updated $W^{(1)}$ and $W^{(2)}$ to represent meaningful intermediate features.
3. **Identical Initialization:** Identical hidden units compute the exact same output and receive the exact same gradient[cite: 6], forcing them to update symmetrically and preventing the network from learning the multiple distinct features needed for XOR.
4. **Gradient Effects:** Sigmoid units saturate easily, contributing small derivatives that shrink the gradient (vanishing gradient problem)[cite: 6]. Active ReLU units contribute a derivative of 1, preserving gradient magnitude through deep layers[cite: 6], but can "die" if the pre-activation falls below zero. 
5. **Output Layer Selection:** The output activation maps the raw network tensor to the domain of the task (e.g., probability), and the loss must mathematically measure the error in that specific domain (e.g., cross-entropy for distributions)[cite: 6].
6. **LLM Usage:** The LLM was highly productive for generating the PyTorch `optim.SGD` loops and `backward()` boilerplates. However, human verification was essential when evaluating the ReLU failure state, as the LLM blindly assumed ReLU would be universally "best" without understanding the dead-neuron risk on a tiny dataset.
7. **Scale Considerations:** Inspecting final loss and validation accuracy scales universally. However, exhaustively printing weight matrices and performing finite-difference gradient checks becomes computationally impossible and practically unreadable when parameters reach the billions[cite: 6].
