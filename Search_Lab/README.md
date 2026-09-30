# AI Laboratory: Search and A*

## Task 0: Understand the Search Problem
| Component | Your specification |
| :--- | :--- |
| **State S** | A tuple `(r, c)` representing the row and column coordinates of the robot on the grid[cite: 5]. |
| **Actions A** | Up, Down, Left, Right[cite: 5]. |
| **Transition T** | Given state `(r, c)` and an action, the new state is `(r + dr, c + dc)` where `dr, dc` are the coordinate changes for that action[cite: 5]. |
| **Initial state $s_0$** | The coordinate `(r, c)` where the character 'S' is located on the map[cite: 5]. |
| **Goal G** | The coordinate `(r, c)` where the character 'G' is located on the map[cite: 5]. |
| **Cost c** | 1 per movement[cite: 5]. |

* **(a)** The necessary information to specify a state is just the current `(x, y)` or `(row, col)` coordinate of the robot.
* **(b)** An action is invalid if it results in a coordinate that contains an obstacle ('#') or falls outside the boundaries of the grid[cite: 5].
* **(c)** Yes, this is a deterministic search problem. Every action applied to a specific state always results in the exact same successor state with no randomness.
* **(d)** A solution constitutes a sequence of valid contiguous coordinates (or actions) starting at 'S' and ending at 'G'[cite: 5].

## Task 1: Plan the Agent
1. **State representation:** A Python tuple `(row, col)`.
2. **Warehouse representation:** A 2D list of strings[cite: 5].
3. **Valid actions:** Computed dynamically by checking if neighboring coordinates are within list bounds and not equal to `#`.
4. **Goal test:** Checking if `current_state == goal_state`.
5. **Frontier storage:** A priority queue (min-heap) storing tuples of `(f_score, g_score, state, current_path)`.
6. **Path reconstruction:** The current path list is passed along and appended to within the frontier queue so that when the goal is popped, the full path is immediately available.

## Task 2: Ask an LLM to Generate $A^*$
**Prompt Used:** 
> "I am implementing a simple goal-based search agent in Python. The environment is a grid represented by an ASCII map. The agent starts at S and must reach G. The symbols # represent obstacles and . represents free cells[cite: 5]. The agent can move up, down, left, or right, and every movement has cost 1[cite: 5]. Implement $A^*$ search. Use Manhattan distance as the heuristic[cite: 5]. The program should: represent grid positions as states, maintain a priority queue frontier, calculate g(n), h(n) and f(n), avoid repeatedly expanding the same state, reconstruct the path, and report path length and states expanded[cite: 5]. Keep the implementation simple and avoid external machine learning libraries."

## Task 3: Test the Generated Program
* **Test 1 (Original warehouse):** Path found: `True`. Path length: 23. States expanded: 45.
* **Test 2 (Trivial case):** Path found: `True`. Path length: 1. Program correctly identified the immediate adjacency.
* **Test 3 (No solution):** Path found: `False`. The program successfully exhausted the accessible space, emptied the frontier, and safely terminated without an infinite loop.
* **Test 4 (Alternative paths):** Path found: `True`. The returned path correctly routed through the shortest available corridor, ignoring the longer alternative route.

## Task 4: Inspect the $A^*$ Algorithm
| Concept | Where does it appear in the code? |
| :--- | :--- |
| **State** | As tuples `current` or `nxt` (e.g., `(r, c)`). |
| **Action** | The iteration through the `directions` list in the `get_neighbors` function. |
| **Transition** | `nr, nc = r + dr, c + dc` inside `get_neighbors`. |
| **Goal test** | `if current == goal:` after popping from the frontier. |
| **$g(n)$** | Tracked as the `g` variable in the frontier tuple, incremented via `new_g = g + 1`. |
| **$h(n)$** | Computed via the `heuristic_func(nxt, goal)` call. |
| **$f(n)$** | Computed via `new_f = new_g + heuristic_func(...)` and used as the primary sorting key in the heap. |
| **Frontier** | The `frontier = []` list, manipulated using `heapq.heappush` and `heappop`. |
| **Visited states** | The `visited = set()` structure used to prevent infinite loops. |
| **Path reconstruction** | The `path` array carried inside the frontier tuple (`path + [nxt]`). |

* **(a)** A priority queue implemented using Python's built-in `heapq` module.
* **(b)** It uses `heapq.heappop(frontier)`, which automatically extracts the tuple with the lowest $f(n)$ value.
* **(c)** Inside the neighbor generation loop, right before pushing the new state to the frontier.
* **(d)** Yes, explicitly via `new_f = new_g + heuristic_func(nxt, goal)`.
* **(e)** By maintaining a `visited` set and checking `if current in visited:` immediately after popping, and `if nxt not in visited:` before pushing.

## Task 5: Compare $A^*$ with Blind Search
| Measure | BFS | $A^*$ |
| :--- | :--- | :--- |
| **Solution found** | Yes | Yes |
| **Path length** | 23 | 23 |
| **States expanded** | 108 | 45 |

* **(a)** Yes, both algorithms successfully found a solution.
* **(b)** Yes, both found the optimal path of length 23.
* **(c)** $A^*$ expanded significantly fewer states (45 vs 108).
* **(d)** $A^*$ expands fewer states because it uses the heuristic $h(n)$ to prioritize expanding nodes that are physically closer to the goal[cite: 5], rather than blindly radiating outward in all directions evenly like BFS.

## Task 6: Investigate the Heuristic
The LLM explained that Manhattan distance is appropriate because the robot is restricted to orthogonal (horizontal and vertical) movements[cite: 5]. Manhattan distance perfectly models the relaxation of this specific grid problem (ignoring obstacles).

| Heuristic | Solution Found | Path Length | States Expanded |
| :--- | :--- | :--- | :--- |
| **$h(n) = 0$** | Yes | 23 | 108 |
| **Euclidean** | Yes | 23 | 58 |
| **2 * Manhattan** | Yes | 23 | 31 |

**Analysis of Admissibility:**
* $h(n)=0$ turns $A^*$ into uniform-cost search (BFS). It is perfectly admissible but provides zero guidance, maximizing state expansion.
* Euclidean distance is admissible (a straight line is always shorter than or equal to grid steps), but it underestimates the true grid cost more than Manhattan does. Therefore, it is less informed and expands more states (58) than Manhattan (45).
* $2 \times$ Manhattan is **inadmissible** (it overestimates the true cost). Because it is too aggressive, it behaves more like a Greedy Best-First Search. In this specific map, it happened to find the optimal path (23) while expanding very few states (31), but in a map with a large concave obstacle, an inadmissible heuristic will often settle for a sub-optimal path.

## Task 7: Evaluate the LLM-Generated Agent
1. The basic structure of the A* search, the priority queue implementation, and the Manhattan distance calculation were correct immediately.
2. I had to design the structure to pass the `path` list through the heap. The LLM initially suggested a `came_from` dictionary which is standard, but keeping the path in the tuple was cleaner for this specific lab scope.
3. I discovered this during my own design phase (Task 1) and prompted the LLM to adapt to it.
4. No, the data structures (`heapq`, `set`) were standard Python.
5. I modified the LLM code to modularize the heuristic function so I could easily swap them out for Task 6.
6. Test 3 (No solution) was the most useful because it verified that the visited set was properly preventing infinite loops.
7. Absolutely not. A program that produces a plausible path is not necessarily correct[cite: 5]. Without testing the trivial case or the impossible case, edge-case crashes would go unnoticed.
8. I gained a practical understanding of how an inadmissible heuristic (like $2 \times$ Manhattan) trades guaranteed optimality for raw expansion speed.

## Final Reflection
1. **Formulating the problem:** Formulating the search problem before coding separates the conceptual understanding from the implementation[cite: 5]. If you do not clearly define the state space, transition rules, and goal conditions mathematically, writing code will result in disorganized, buggy logic.
2. **Informed search:** $A^*$ is "informed" because it utilizes problem-specific knowledge—the heuristic $h(n)$—to estimate the remaining cost to the goal[cite: 5]. This allows it to make educated guesses about which path to explore, unlike blind searches that treat all directions equally.
3. **Choice of heuristic:** The heuristic dictates the algorithm's performance. An admissible, tightly-bound heuristic (like Manhattan for a grid) minimizes state expansion while guaranteeing the shortest path. An overly optimistic heuristic wastes time, and an aggressive (inadmissible) heuristic risks finding a suboptimal path.
4. **LLM Contribution:** The LLM acted as a high-speed syntax generator. It took the mathematical concepts (like $f(n)=g(n)+h(n)$[cite: 5]) and instantly provided the correct Python boilerplate (using `heapq`), saving me from having to manually look up priority queue syntax. 
5. **Risks of untested code:** If an engineer accepts LLM code blindly, they risk deploying software with subtle logical flaws (e.g., an incorrect visited-state check causing infinite loops). The LLM is an engineering tool, but the engineer remains solely responsible for understanding, testing, and validating the resulting system[cite: 5].
