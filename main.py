# main.py
import random
import matplotlib.pyplot as plt
import numpy as np
from salesman import Salesman
from city import City
from plotting import plot_best_cost_progress, plot_cities_and_tour
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
    #slow_time
    #
    #dif_parameters = [1.01, 2, 5] # slow_time
    #dif_parameters = [7, 9, 12, 22] # current_time
    #dif_parameters = [50] #  fuel_cost_per_liter
    dif_parameters = [60, 80, 100] #   initial_velocity
    #dif_parameters = [200]#  price per hour
    # Lists to store the results for each slow_time value
    number_of_average = 20

    average_best_cost = []
    squared_best_cost = []
    for parameters in dif_parameters:

        best_cost_progress_list = []
        copied_parameters= [parameters]*number_of_average
        number = 0
        for parameter in copied_parameters:
            number+=1
            salesman.optimal_route = cities[:]
            # Set the parameter
            #salesman.slow_time = parameter #slow_time
            #salesman.current_time = parameter #current_time
            #salesman.fuel_cost_per_liter = parameter #fuel_cost_per_liter
            salesman.initial_velocity = parameter #initial_velocity
            #salesman.hourly_salary = parameter #hourly_salary
            # Run the simulated annealing algorithm
            initial_temperature = 10**8
            cooling_rate = 0.01
            iterations = 3000
            

            best_cost, best_cost_progress, temperature_progress = simulated_annealing(salesman, initial_temperature, cooling_rate, iterations)
            print(f"Best cost found by simulated annealing with slow_time={parameter} (number {number} of {len(copied_parameters)}): {best_cost}")
            #plot_cities_and_tour(salesman.cities,salesman.optimal_route)
            # Store the results for plotting
            best_cost_progress_list.append(best_cost_progress)
        #plot_best_cost_progress(temperature_progress, best_cost_progress_list, squared_best_cost, copied_parameters,plot_average=True)
        average_best_cost.append(np.mean(best_cost_progress_list, axis=0))   
        squared_best_cost.append(np.mean(np.square(best_cost_progress_list),axis=0)) 
    # Plot the best cost progress over temperature for all slow_time values
    #plot_cities_and_tour(salesman.cities,salesman.optimal_route)
    plot_best_cost_progress(temperature_progress, average_best_cost,  squared_best_cost, dif_parameters,plot_average=False, C_func = True)

if __name__ == "__main__":
    main()