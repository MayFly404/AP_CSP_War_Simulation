import random

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

def evaluate_situation(countries, grid: list, logs: bool):
    neighbors_map = {}

    # Calculate neighbors for all countries
    for country in countries:
        neighbors_map[country.country_id] = get_neighbors(country.country_id, grid)
        country.power += (3 * len(country.territories))

        for enemy in country.enemies:
            country.morale += 2

        
        
        if country.morale <= 15 and country.stability <= 15:
            country.die(grid)


    if logs: print("Neighbors Map:", neighbors_map)

    for country in countries:
        for enemy_id in country.enemies:
            if enemy_id in neighbors_map[country.country_id]:
                defender_country = next((c for c in countries if c.country_id == enemy_id), None)
                if defender_country:
                    # Find bordering territories
                    defender_territories = [
                        (i, j) for i, row in enumerate(grid)
                        for j, cell in enumerate(row)
                        if cell == enemy_id and
                        any(grid[i + dx][j + dy] == country.country_id
                            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                            if 0 <= i + dx < len(grid) and 0 <= j + dy < len(grid[0]))
                    ]
                    if defender_territories:
                        defender_territory = random.choice(defender_territories)
                        attack(country, defender_country, defender_territory, grid, logs)

    for country in countries:
        country_neighbors = [c for c in countries if c.country_id in neighbors_map[country.country_id]]
        decide_treaty(country, country_neighbors, logs)  # Check treaties after losses/gains
        ally(country, country_neighbors, logs)  # Handle alliances
        decide_war(country, country_neighbors, logs)
        print(f"Country {country.country_id} has {len(country.territories)} territories")



def attack(attacker, defender: list, defender_territory: tuple, grid: list, logs: bool):
    # Get attacker's neighboring territories
    neighboring_territories = set()
    for x, y in attacker.territories:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == defender.country_id:
                neighboring_territories.add((nx, ny))
    
    # Check if the defender territory is a valid neighboring territory
    if defender_territory not in neighboring_territories:
        if logs: print(f"{attacker.country_id} cannot attack {defender_territory} as it is not a bordering territory.")
        return
    
    attacker_dies = sorted([random.randint(1, 7) for _ in range(3)])  # Roll 3 attacker dice
    defender_dies = sorted([random.randint(1, 7) for _ in range(2)])  # Roll 2 defender dice
    
    momentum = 0
    if attacker_dies[0] > defender_dies[0]:
        defender.power -= 50
        momentum += 1
        if logs: print(f"{attacker.country_id} won the first roll against {defender.country_id}.")
    else:
        attacker.power -= 50
        if logs: print(f"{attacker.country_id} lost the first roll against {defender.country_id}.")
    
    if attacker_dies[1] > defender_dies[1]:
        defender.power -= 50
        momentum += 1
        if logs: print(f"{attacker.country_id} won the second roll against {defender.country_id}.")
    else:
        attacker.power -= 50
        if logs: print(f"{attacker.country_id} lost the second roll against {defender.country_id}.")
    
    if momentum == 2:  # Attacker wins both rolls
        # Update grid
        x, y = defender_territory
        grid[x][y] = attacker.country_id
    
        # Update territories
        attacker.annex_territory(x, y)
        
        defender.morale -= 5
        defender.stability -= 5
    
        if logs: print(f"{attacker.country_id} annexed territory {defender_territory} from {defender.country_id}.")
    
        # Check if defender has no territories left
        if not defender.territories:
            defender.die(grid)
            if logs: print(f"{defender.country_id} has been eliminated!")
    else:
        if logs: print(f"{attacker.country_id} failed to annex territory {defender_territory} from {defender.country_id}.")
    
    

def decide_war(country, neighbors: list, logs: bool):
    for neighbor in neighbors:
        if country.country_id in neighbor.enemies:
    
            continue
    
        if len(neighbor.territories) > len(country.territories):
            if len(country.territories) * 1.5 < len(neighbor.territories):
                if logs: print(f"{neighbor.country_id} too big for war")
            elif (country.power * 1.25) <= neighbor.power:
                if logs: print(f"{neighbor.country_id} too strong for war")
            else:
                if logs: print(f"{country.country_id} declaring war on {neighbor.country_id}")
                country.enemies.append(neighbor.country_id)
                neighbor.enemies.append(country.country_id)  # Ensure bidirectional war declaration
        else:
            print(f"{country.country_id} declaring war on {neighbor.country_id}")
            country.enemies.append(neighbor.country_id)
            neighbor.enemies.append(country.country_id)  # Ensure bidirectional war declaration

def ally(country, neighbors: list, logs: bool):
    for neighbor in neighbors:
        if country.country_id in neighbor.allies:
            if logs: print(f"{country.country_id} is already allied with {neighbor.country_id}")
            continue

        if country.country_id in neighbor.enemies or neighbor.country_id in country.enemies:
            if logs: print(f"{country.country_id} cannot ally with {neighbor.country_id} due to existing conflict")
            continue

        # Check for common enemy
        common_enemies = set(country.enemies).intersection(set(neighbor.enemies))
        if not common_enemies:
            if logs: print(f"{country.country_id} and {neighbor.country_id} have no common enemies")
            continue

        # Check for similar economies, stability, and land sizes
        if abs(country.economy - neighbor.economy) / max(country.economy, neighbor.economy) > 0.2:
            if logs: print(f"{country.country_id} and {neighbor.country_id} have too different economies")
            continue

        if abs(country.stability - neighbor.stability) > 10:
            if logs: print(f"{country.country_id} and {neighbor.country_id} have too different stabilities")
            continue

        if abs(country.land_size - neighbor.land_size) / max(country.land_size, neighbor.land_size) > 0.2:
            if logs: print(f"{country.country_id} and {neighbor.country_id} have too different land sizes")
            continue

        print(f"{country.country_id} proposes an alliance with {neighbor.country_id}")
        country.allies.append(neighbor.country_id)
        neighbor.allies.append(country.country_id)  # Ensure bidirectional treaty


def decide_treaty(country, neighbors: list, logs: bool):
    for neighbor in neighbors:
        if neighbor.country_id in country.enemies:
            # Check if the country has lost or taken more than 5 territories
            if neighbor.land_taken.get(country, 0) >= 5 or country.land_taken.get(neighbor, 0) >= 5:
                # Make peace
                country.enemies.remove(neighbor.country_id)
                neighbor.enemies.remove(country.country_id)
                country.treaties.append(neighbor.country_id)
                neighbor.treaties.append(country.country_id)
                country.land_taken[neighbor] = 0  # Reset land taken counter
                neighbor.land_taken[country] = 0
                if logs: print(f"{country.country_id} and {neighbor.country_id} made a treaty after territorial losses or gains.")
            else:
                if logs: print(f"{country.country_id} and {neighbor.country_id} are still at war.")
