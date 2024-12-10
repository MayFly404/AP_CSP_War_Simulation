import psycopg2
import os
import random

from objects import *
from country_algorithm import *

database_url = os.environ['DATABASE_URL']


countries = {}

grid = []


def create_grid(size: int) -> list:
    """
    Creates a grid of the specified size.

    Args:
        size (int): The size of the grid.

    Returns:
        list: A list of lists representing the grid.
    """
    
    for row in range(size):
        grid.append([0] * size)

    return grid

def split_grid(grid: list, countries: list) -> list:
    """
    Splits a grid into territories and assigns them to countries, retaining the original grid's shape.

    Args:
        grid (list): A 2D list representing the grid to be divided. Each element 
                     of the grid is a row containing cells.
        countries (list): A list of unique country identifiers (strings or other values)
                          that represent the countries to which the grid territories 
                          will be assigned.

    Returns:
        list: A new 2D list (grid) with the same dimensions as the input grid,
              where each cell contains the country assigned to that territory.
              If `countries` is empty, the original grid is returned unchanged.
    """
    if not countries:
        return grid

    rows: int = len(grid)          # Number of rows in the grid
    cols: int = len(grid[0])       # Number of columns in the grid
    total_cells: int = rows * cols # Total number of cells in the grid
    country_count: int = len(countries)

    # Calculate the number of cells each country should occupy
    cells_per_country: int = total_cells // country_count
    extra_cells: int = total_cells % country_count

    # Flatten the grid into a list of cells for assignment
    flat_grid = [None] * total_cells
    current_country_index = 0
    cell_count = 0

    # Assign each cell to a country, distributing extra cells as needed
    for i in range(total_cells):
        flat_grid[i] = countries[current_country_index]
        cell_count += 1

        # Move to the next country when its quota is filled
        if cell_count >= cells_per_country + (1 if extra_cells > 0 else 0):
            cell_count = 0
            current_country_index += 1
            if extra_cells > 0:
                extra_cells -= 1

    # Reshape the flat list back into the original grid dimensions
    divided_grid = [
        flat_grid[row * cols:(row + 1) * cols] for row in range(rows)
    ]

    return divided_grid

def generate_random_country(country_id: int) -> Country:
    country = Country(
        country_id=country_id,
        name=f"Country-{country_id}",
        economy=random.randint(1000, 100000),
        power=random.randint(100, 1000),
        morale=random.randint(1, 100),
        stability=random.randint(1, 100),
        population=random.randint(100000, 100000000),
        land_size=0 # initialized to 0 but changed later
    )
    # Add to global dictionary
    countries[country_id] = country
    return country


def init_game() -> (list, list):
    """

    The init_game function first creats the grid using the `create_grid` function,
    then it calculates the number of territories needed to be allocated to each
    country outlined in `countries.` Then, it splits the board and spits out
    the new one.
    
    """
    grid_size = 10
    grid = create_grid(grid_size)
    
    number_of_countries = 60
    
    generated_countries = [generate_random_country(i) for i in range(1, number_of_countries + 1)]
    country_ids = [c.country_id for c in generated_countries if c is not None]
    
    divided_grid = split_grid(grid, country_ids)
    
    for row in divided_grid:
        print(' '.join(str(cell) for cell in row))
    
    for country in generated_countries:
        territories = [(i, j) for i, row in enumerate(divided_grid) for j, c_id in enumerate(row) if c_id == country.country_id]
        for x, y in territories:
            country.annex_territory(x, y)

    return divided_grid, generated_countries
    

if __name__ == "__main__":
    divided_grid, generated_countries = init_game()

    country_ids = [country.country_id for country in generated_countries if country is not None]
    
    for country_id in country_ids:
        print(f"Country-{country_id}: Country-{evaluate_situation(country_id, divided_grid)}")