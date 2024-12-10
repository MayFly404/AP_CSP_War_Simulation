import psycopg2
import os
from objects import Country
import random

database_url = os.environ['DATABASE_URL']

def generate_random_country(country_id: int) -> Country:
    return Country(
        country_id=country_id,
        name=f"Country-{country_id}",
        economy=random.randint(1000, 100000),
        power=random.randint(100, 1000),
        morale=random.randint(1, 100),
        stability=random.randint(1, 100),
        population=random.randint(100000, 100000000),
        land_size=0
    )

def insert_countries_to_db(countries):
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    try:
        for country in countries:
            cur.execute("""
                INSERT INTO Countries (CountryID, Name, Economy, Power, Morale, Stability, Population, LandSize)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (CountryID) DO NOTHING
            """, (country.country_id, country.name, country.economy, country.power, country.morale, country.stability,
                  country.population, country.land_size))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def main():
    number_of_countries = 5
    countries = [generate_random_country(i) for i in range(1, number_of_countries + 1)]

    insert_countries_to_db(countries)
    print("Countries have been initialized and saved to the database.")

if __name__ == "__main__":
    main()