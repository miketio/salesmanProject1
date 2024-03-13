# main.py
import random
import matplotlib.pyplot as plt
import numpy as np
from salesman import Salesman
from city import City
from plotting import plot_best_cost_progress
from MCmethods import simulated_annealing

def load_cities_from_file(file_path):
    cities = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y, weight = map(int, line.strip().split())
            cities.append(City(x, y, weight))
    return cities


def main():
    # Define a list of cities with their coordinates and package weights
    # Использование функции для загрузки городов из файла
    cities = load_cities_from_file('cities.txt')

    # Check if the list of cities is empty
    if not cities:
        print("No cities provided.")
        return

    # Initialize the salesman with the list of cities
    salesman = Salesman(cities)

    # List of slow_time values to test
    slow_times= [1.25] * 10 #slow_times = [1.01, 1.25, 1.3, 1.4, 1.5, 1.6, 1.75, 1.8, 2, 10]
    # Lists to store the results for each slow_time value
    temperature_progress_list = []
    best_cost_progress_list = []

    for slow_time in slow_times:
        # Set the slow_time parameter
        salesman.slow_time = slow_time

        # Run the simulated annealing algorithm
        initial_temperature = 10**8
        cooling_rate = 0.005
        iterations = 3000
        best_cost, best_cost_progress, temperature_progress = simulated_annealing(salesman, initial_temperature, cooling_rate, iterations)
        print(f"Best cost found by simulated annealing with slow_time={slow_time}: {best_cost}")

        # Store the results for plotting
        best_cost_progress_list.append(best_cost_progress)
        temperature_progress_list.append(temperature_progress)
        salesman.optimal_route = cities[:]
    # Plot the best cost progress over temperature for all slow_time values
    plot_best_cost_progress(temperature_progress_list, best_cost_progress_list, slow_times,plot_average=True)

if __name__ == "__main__":
    main()