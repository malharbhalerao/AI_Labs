import heapq
from collections import deque
import math

# --- Maps ---
map_original = [
    "#################",
    "#S....#.......#.#",
    "#.###.#.#######.#",
    "#...#.#.......#.#",
    "###.#.#######.#.#",
    "#...#.........#.#",
    "#.###########.#.#",
    "#........#G#..#.#",
    "#################"
]

map_trivial = [
    "#####",
    "#SG##",
    "#####"
]

map_no_solution = [
    "#######",
    "#S....#",
    "###.###",
    "#...#G#",
    "#######"
]

map_alternative = [
    "#######",
    "#S....#",
    "#.###.#",
    "#....G#",
    "#######"
]

# --- Helper Functions ---
def parse_grid(grid):
    start, goal = None, None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 'S': start = (r, c)
            if val == 'G': goal = (r, c)
    return start, goal, grid

def get_neighbors(r, c, grid):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            neighbors.append((nr, nc))
    return neighbors

# --- Heuristics ---
def h_manhattan(curr, goal):
    return abs(curr[0] - goal[0]) + abs(curr[1] - goal[1])

def h_zero(curr, goal):
    return 0

def h_euclidean(curr, goal):
    return math.sqrt((curr[0] - goal[0])**2 + (curr[1] - goal[1])**2)

def h_double_manhattan(curr, goal):
    return 2 * (abs(curr[0] - goal[0]) + abs(curr[1] - goal[1]))

# --- A* Search ---
def a_star_search(grid, heuristic_func=h_manhattan):
    start, goal, _ = parse_grid(grid)
    if not start or not goal: return False, [], 0, 0

    # Frontier stores: (f_score, g_score, (r, c), path)
    frontier = []
    heapq.heappush(frontier, (0 + heuristic_func(start, goal), 0, start, [start]))
    
    visited = set()
    states_expanded = 0

    while frontier:
        f, g, current, path = heapq.heappop(frontier)

        if current in visited:
            continue
            
        visited.add(current)
        states_expanded += 1

        if current == goal:
            return True, path, len(path)-1, states_expanded

        for nxt in get_neighbors(current[0], current[1], grid):
            if nxt not in visited:
                new_g = g + 1
                new_f = new_g + heuristic_func(nxt, goal)
                heapq.heappush(frontier, (new_f, new_g, nxt, path + [nxt]))

    return False, [], 0, states_expanded

# --- BFS Search ---
def bfs_search(grid):
    start, goal, _ = parse_grid(grid)
    if not start or not goal: return False, [], 0, 0

    frontier = deque([(start, [start])])
    visited = set([start])
    states_expanded = 0

    while frontier:
        current, path = frontier.popleft()
        states_expanded += 1

        if current == goal:
            return True, path, len(path)-1, states_expanded

        for nxt in get_neighbors(current[0], current[1], grid):
            if nxt not in visited:
                visited.add(nxt)
                frontier.append((nxt, path + [nxt]))

    return False, [], 0, states_expanded

# --- Execution ---
if __name__ == "__main__":
    print("--- Test 1: Original Warehouse (A* Manhattan) ---")
    found, path, length, expanded = a_star_search(map_original)
    print(f"Found: {found}, Length: {length}, Expanded: {expanded}")

    print("\n--- BFS vs A* Comparison (Original Map) ---")
    found_bfs, _, len_bfs, exp_bfs = bfs_search(map_original)
    print(f"BFS -> Length: {len_bfs}, Expanded: {exp_bfs}")
    print(f"A*  -> Length: {length}, Expanded: {expanded}")

    print("\n--- Heuristic Investigation (Original Map) ---")
    _, _, l1, e1 = a_star_search(map_original, h_zero)
    print(f"h=0 (Dijkstra)     -> Length: {l1}, Expanded: {e1}")
    _, _, l2, e2 = a_star_search(map_original, h_euclidean)
    print(f"h=Euclidean        -> Length: {l2}, Expanded: {e2}")
    _, _, l3, e3 = a_star_search(map_original, h_double_manhattan)
    print(f"h=2*Manhattan      -> Length: {l3}, Expanded: {e3}")
