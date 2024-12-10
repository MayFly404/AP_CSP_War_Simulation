
def get_neighbors(country_id: int, grid: list) -> set:
    neighbors = set()

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == country_id:
                for direction in directions:
                    ni, nj = i + direction[0], j + direction[1]
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighboring_country = grid[ni][nj]
                        if neighboring_country != country_id:
                            neighbors.add(neighboring_country)

    return neighbors

def evaluate_situation(country_id: int, grid: list):
    neighbors = get_neighbors(country_id, grid)
    
    return neighbors

def decide_war(country_id: int):
    pass