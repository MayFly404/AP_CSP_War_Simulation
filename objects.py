class Country:
    def __init__(
        self,
        country_id=None,
        name="",
        economy=0,
        power=0,
        allies=[],
        enemies=[],
        treaties=[],
        morale=0,
        stability=0,
        starting_territories = 0,
        population=0,
        land_size=0,
        territories=[],
        land_taken={}
    ):
        self.country_id = country_id
        self.name = name
        self.economy = economy
        self.power = power
        self.allies = allies
        self.enemies = enemies
        self.treaties = treaties
        self.morale = morale
        self.stability = stability
        self.starting_territories = 0,
        self.population = population
        self.land_size = land_size
        self.territories = []
        self.land_taken = land_taken

    def annex_territory(self, x, y):
        """Annex a new territory to the in-memory territories list."""
        if (x, y) not in self.territories:
            self.territories.append((x, y))
            self.land_size += 1

    def die(self, grid):
        """Clears the country's data, simulating removal."""
        for x, y in self.territories:
            grid[x][y] = "🔥"
        self.territories.clear()
        self.land_size = 0

    def __repr__(self):
        return (f"Country(country_id={self.country_id}, name={self.name}, economy={self.economy}, "
                f"power={self.power}, allies={self.allies}, enemies={self.enemies}, treaties={self.treaties}, "
                f"morale={self.morale}, stability={self.stability}, population={self.population}, "
                f"land_size={self.land_size}, territories={self.territories})")