# AI Laboratory: Logical Reasoning for Planning

## Task 0: Understand the Planning Problem
* **(a) Initial State $I$**: `{At(Robot, A), At(Package, A)}`[cite: 4].
* **(b) Goal $G$**: `{At(Package, C)}`[cite: 4].
* **(c) Available Actions**: Move(Loc1, Loc2), PickUp(Item, Loc), Drop(Item, Loc)[cite: 4].
* **(d) Preconditions and Effects**:
  * *Move(A, B)*: Pre = `{At(Robot, A)}`, Effects = `{-At(Robot, A), At(Robot, B)}`[cite: 4].
  * *PickUp(Package, A)*: Pre = `{At(Robot, A), At(Package, A)}`, Effects = `{-At(Package, A), Holding(Package)}`[cite: 4].
  * *Drop(Package, C)*: Pre = `{At(Robot, C), Holding(Package)}`, Effects = `{-Holding(Package), At(Package, C)}`[cite: 4].
* **Question Applicability**: 
  * `PickUp(Package, A)` is **applicable** because both its preconditions (`At(Robot, A)` and `At(Package, A)`) are present in the initial state[cite: 4]. 
  * `Drop(Package, C)` is **not applicable** because its preconditions (`At(Robot, C)` and `Holding(Package)`) are missing from the initial state[cite: 4].

## Task 1: Construct a Plan by Hand
| State | Facts | Action Taken to Reach Next State |
| :--- | :--- | :--- |
| **$S_0$** | At(Robot, A), At(Package, A)[cite: 4] | PickUp(Package, A)[cite: 4] |
| **$S_1$** | At(Robot, A), Holding(Package) | Move(A, B)[cite: 4] |
| **$S_2$** | At(Robot, B), Holding(Package) | Move(B, C)[cite: 4] |
| **$S_3$** | At(Robot, C), Holding(Package) | Drop(Package, C)[cite: 4] |
| **$S_4$** | At(Robot, C), At(Package, C) | *(Goal Achieved)* |

## Task 2: LLM Prompt
> "I want to implement a simple planning agent in Python. Represent a state as a set of logical propositions. Each action should contain a name, positive/negative preconditions, and positive/negative effects. An action is applicable if all of its preconditions are satisfied by the current state. When applied: remove negative effects, add positive effects. Use breadth-first search to find a sequence of actions that achieves a specified goal. The program should detect when no plan exists, print the sequence, and print the states reached after each action."[cite: 4]

## Task 3: Test Results
* **Test A (Solvable Problem):** The planner found a valid 4-step plan matching the hand-traced plan in Task 1. The plan is strictly valid because it successfully achieved `{At(Package, C)}`[cite: 4].
* **Test B (Impossible Problem):** With `PickUp` actions removed, the planner successfully explored the space, recognized the goal was unreachable, and reported "No plan found"[cite: 4].
* **Test C (Irrelevant Actions):** The planner did not confuse the robot reaching C with the package reaching C. It ignored paths where the robot moved empty-handed because BFS prioritizes the shortest path to satisfy the actual goal constraints[cite: 4].

## Task 4: Logic and Search
* **Completed Diagram:** 
  Current state $\rightarrow$ Check action preconditions $\rightarrow$ **Are preconditions met?** $\rightarrow$ Generate successor state $\rightarrow$ Search over alternatives $\rightarrow$ Goal?[cite: 4].
* **Explanation:** Logic is used at the micro-level to determine if an action is valid (checking preconditions against the state) and to generate the exact resulting state (applying effects)[cite: 4]. Search is used at the macro-level to organize these logical transitions into a tree and systematically traverse it to find a path to the goal[cite: 4].

## Task 5: LLM Verification
* **Question:** Which should you trust more?
* **Answer:** (b) The independently executed state transitions[cite: 4]. An LLM generates an explanation probabilistically based on linguistic patterns, which can hallucinate false logic that "sounds" correct. Independent code execution forces strict mathematical and logical validation where a missing precondition physically prevents execution.

## Task 5: Reflection Questions
1. Specifying conditions heavily restricts the LLM from hallucinating "magic" actions (e.g., teleporting the package) and forces it to map exact state variables[cite: 4].
2. If the planner failed to check preconditions, it might execute `Drop(Package, C)` while the robot is still at location A, resulting in the package illegally materializing at C.
3. A plan might "look reasonable" to a human reader but violate strict logical constraints (e.g., dropping an item you never explicitly picked up)[cite: 4].
4. The LLM provided the Python boilerplate, the BFS loop implementation, and the state-copying logic. 
5. I had to independently verify the exact propositions, ensuring the state transitions matched logical rules and that the loop actually terminated properly.
6. Logical reasoning is used inside the `is_applicable` and `apply` methods of the `Action` class[cite: 4].
7. Planning maps directly to search algorithms: the state is the node, the logical actions are the edges (transitions), and the planner runs standard BFS to find the goal node[cite: 4].

## Optional Extension: Prolog as a Logical Verifier
### Task 6: Plan Verifier
* **(a)** Prolog returns true for `can_move(a,b)` because the fact `connected(a,b)` is explicitly defined in the knowledge base, satisfying the rule `can_move(X,Y) :- connected(X,Y)`[cite: 4].
* **(b)** It does not establish `can_move(a,c)` because there is no direct `connected(a,c)` fact, and the rule does not account for multi-step transitivity[cite: 4].
* **(c)** The Prolog rule `can_move(X,Y) :- connected(X,Y)` is the exact programmatic implementation of the logical implication $Connected(X,Y) \rightarrow CanMove(X,Y)$[cite: 4].

### Task 8: Prolog Inference
* **Explanation:** The query `?- reduce_speed` succeeds because Prolog traces it backward: `reduce_speed` requires `slippery`, which requires `wet_road`, which is stated as a base fact[cite: 4]. 
* **Implications:** `Fact: wet_road` $\rightarrow$ `Rule: slippery :- wet_road` $\rightarrow$ `Rule: reduce_speed :- slippery` $\rightarrow$ `Conclusion: reduce_speed` is true[cite: 4].

### Reflection (Prolog)
1. A fact is a declarative truth with no conditions (e.g., `wet_road`), while a rule relies on conditions being met to establish a truth (e.g., `slippery :- wet_road`)[cite: 4].
2. A query asks the Prolog engine to use its internal inference engine to traverse known facts and rules to see if the queried statement logically entails from the knowledge base[cite: 4].
3. A Python program might contain a bug in its state-generation logic. Prolog, being a dedicated inference engine, can independently verify if a Python-generated sequence strictly adheres to logical rules[cite: 4].
4. An independent verifier provides deterministic, mathematically sound proof of correctness, compensating for the LLM's non-deterministic, probabilistic generation[cite: 4].
