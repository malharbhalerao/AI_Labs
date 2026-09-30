from collections import deque

# The warehouse map represented as a 2D grid
raw_map = [
    "#####################",
    "#S....#..G#.........#",
    "#.##.....##########.#",
    "#....##.......#.....#",
    "#.######.###.#.###..#",
    "#.......#.........#.#",
    "#####################"
]

def parse_grid(grid):
    start, goal = None, None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 'S': start = (r, c)
            if val == 'G': goal = (r, c)
    return start, goal, grid

def solve_warehouse(grid):
    start, goal, matrix = parse_grid(grid)
    if not start or not goal:
        return "Missing Start (S) or Goal (G) in the map."

    queue = deque([(start, [])])
    visited = set([start])
    
    # Up, Down, Left, Right moves
    directions = {
        'Up': (-1, 0), 'Down': (1, 0), 
        'Left': (0, -1), 'Right': (0, 1)
    }

    while queue:
        (current_r, current_c), path = queue.popleft()
        
        if (current_r, current_c) == goal:
            return path
            
        for move_name, (dr, dc) in directions.items():
            nr, nc = current_r + dr, current_c + dc
            
            # Check boundaries and obstacles
            if (0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]) 
                and matrix[nr][nc] != '#' 
                and (nr, nc) not in visited):
                
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [move_name]))
                
    return "No valid path exists."

if __name__ == "__main__":
    print("Warehouse Map:")
    for row in raw_map: print(row)
    
    path = solve_warehouse(raw_map)
    print("\nResulting Path:", path)
    if isinstance(path, list):
        print(f"Total steps: {len(path)}")
