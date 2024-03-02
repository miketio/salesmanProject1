# main.py
import random
from salesman import Salesman
from city import City
from plotting import plot_cities_and_tour

def main():
    # Define a list of cities with their coordinates and package weights
    cities = [
        City(random.randint(0, 100), random.randint(0, 100), random.randint(1, 5)) for _ in range(10)
    ]

    # Check if the list of cities is empty
    if not cities:
        print("No cities provided.")
        return

    # Initialize the salesman with the list of cities
    salesman = Salesman(cities)

    # Run the simulated annealing algorithm
    initial_temperature = 1000
    cooling_rate = 0.003
    iterations = 1000
    best_cost = salesman.simulated_annealing(initial_temperature, cooling_rate, iterations)
    print(f"Best cost found: {best_cost}")
    best_cost = salesman.metropolis_hastings(1000)
    print(f"Best cost found: {best_cost}")

    # Plot the cities and the optimal tour
    plot_cities_and_tour(cities, salesman.optimal_route)

if __name__ == "__main__":
    main()