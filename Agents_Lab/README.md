# AI Laboratory: Goal-Based Agents

## Task 1 - Understanding the Problem
1. **Environment:** A two-dimensional grid representing a warehouse[cite: 3]. The environment is fully observable, deterministic, and discrete.
2. **Goal:** The agent must find a collision-free path from the starting position ('S') to the goal position ('G')[cite: 3].
3. **Actions:** The agent can move Up, Down, Left, or Right by one grid square at a time[cite: 3].
4. **Maintained Information:** The agent must maintain its current coordinates, the coordinates of the goal, the layout of the obstacles ('#'), and a record of previously visited states to avoid infinite loops.
5. **Agent Type:** A simple reflex agent only acts based on the current state (its current square), which cannot solve a maze. This is a goal-based agent because it explicitly models the future consequences of its actions to plan a sequence of moves towards the objective[cite: 3].
6. **Think About It:** If the warehouse doubled in size, the state space would expand significantly[cite: 3]. While BFS would still find the optimal path, it would consume more memory and time. An informed search algorithm like A* (using Manhattan distance) would be more appropriate.

## Task 2 - Designing the Agent
**Block Diagram Description:**
* **Sensors:** Reads the initial 2D grid array[cite: 3].
* **State Maintenance:** Tracks `visited` coordinates and the `current_position`.
* **Goal Formulation:** Checks if `current_position == 'G'`.
* **Decision Component (Planner):** Uses Breadth-First Search (BFS) in a `while` loop to evaluate available moves ('Up', 'Down', 'Left', 'Right')[cite: 3].
* **Actuators:** Outputs the final list of sequential directions to navigate the grid.

## Task 3 - Prompt Engineering
1. **Initial Result:** The LLM successfully generated a working program on the first attempt when provided with clear constraints regarding the grid structure and movement rules[cite: 3].
2. **Prompt Improvement:** If the LLM failed, the prompt could be improved by explicitly forbidding diagonal movements or asking it to strictly enforce array boundary checks. 
3. **Algorithm Chosen:** Breadth-First Search (BFS) using a double-ended queue.
4. **Justification:** BFS is optimal for unweighted graph traversals. Because every movement costs exactly one step, BFS guarantees that the first path it finds to the goal is the shortest possible collision-free path.
