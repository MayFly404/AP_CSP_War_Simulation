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

def evaluate_situation(countries, grid: list):
    neighbors_map = {}

    for country in countries:
        neighbors_map[country.country_id] = get_neighbors(country.country_id, grid)

    print(neighbors_map)

    for country in countries:
        country_neighbors = [c for c in countries if c.country_id in neighbors_map[country.country_id]]
        decide_treaty(country, country_neighbors)
        decide_war(country, country_neighbors)

def decide_war(country, neighbors: list):
    for neighbor in neighbors:
        if country.country_id in neighbor.enemies:
    
            continue
    
        if len(neighbor.territories) > len(country.territories):
            if len(country.territories) * 1.5 < len(neighbor.territories):
                print(f"{neighbor.country_id} too big for war")
            elif (country.power * 1.25) <= neighbor.power:
                print(f"{neighbor.country_id} too strong for war")
            else:
                print(f"{country.country_id} declaring war on {neighbor.country_id}")
                country.enemies.append(neighbor.country_id)
                neighbor.enemies.append(country.country_id)  # Ensure bidirectional war declaration
        else:
            print(f"{country.country_id} declaring war on {neighbor.country_id}")
            country.enemies.append(neighbor.country_id)
            neighbor.enemies.append(country.country_id)  # Ensure bidirectional war declaration

def decide_treaty(country, neighbors: list):
    for neighbor in neighbors:
        if country.country_id in neighbor.allies:
            print(f"{country.country_id} is already allied with {neighbor.country_id}")
            continue

        if country.country_id in neighbor.enemies or neighbor.country_id in country.enemies:
            print(f"{country.country_id} cannot ally with {neighbor.country_id} due to existing conflict")
            continue

        # Check for common enemy
        common_enemies = set(country.enemies).intersection(set(neighbor.enemies))
        if not common_enemies:
            print(f"{country.country_id} and {neighbor.country_id} have no common enemies")
            continue

        # Check for similar economies, stability, and land sizes
        if abs(country.economy - neighbor.economy) / max(country.economy, neighbor.economy) > 0.2:
            print(f"{country.country_id} and {neighbor.country_id} have too different economies")
            continue

        if abs(country.stability - neighbor.stability) > 10:
            print(f"{country.country_id} and {neighbor.country_id} have too different stabilities")
            continue

        if abs(country.land_size - neighbor.land_size) / max(country.land_size, neighbor.land_size) > 0.2:
            print(f"{country.country_id} and {neighbor.country_id} have too different land sizes")
            continue

        print(f"{country.country_id} proposes a treaty with {neighbor.country_id}")
        country.allies.append(neighbor.country_id)
        neighbor.allies.append(country.country_id)  # Ensure bidirectional treaty
