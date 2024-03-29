# main.py
import random
import matplotlib.pyplot as plt
import numpy as np
from salesman import Salesman
from city import City
from plotting import plot_best_cost_progress, plot_cities_and_tour, plot_salaries, plot_over_param
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
    cities = load_cities_from_file('cities_small.txt')

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
    dif_parameters = [0,1,2,3,4,5,6,7,8 ,9,10,11, 12,13,14,15,16,17,18,19,20,21,22,23] # current_time
    #dif_parameters = [50] #  fuel_cost_per_liter
    #dif_parameters = [40,50,60,70,80,90] #   initial_velocity
    #dif_parameters = [200]#  price per hour
    # Lists to store the results for each slow_time value
    number_of_average = 20

    average_best_cost = []
    squared_best_cost = []
    average_time_cost = []
    average_salary = []
    average_gas = []
    average_best_cost_resid = []
    
    for parameters in dif_parameters:
        best_cost_list = []
        best_cost_progress_list = []
        time_progress_list = []
        salary_progress_list = []
        gas_progress_list = []
        copied_parameters= [parameters]*number_of_average
        number = 0
        #salesman.optimal_route = cities[:]
        for parameter in copied_parameters:
            number+=1
            salesman.optimal_route = cities[:]
            # Set the parameter
            #salesman.slow_time = parameter #slow_time
            salesman.current_time = parameter #current_time
            #salesman.fuel_cost_per_liter = parameter #fuel_cost_per_liter
            #salesman.initial_velocity = parameter #initial_velocity
            #salesman.hourly_salary = parameter #hourly_salary
            # Run the simulated annealing algorithm
            initial_temperature = 1e6
            cooling_rate = 5e-3
            iterations = 10000
            

            best_cost, best_cost_progress, temperature_progress, time_progress, salary_progress, gas_progress = simulated_annealing(salesman, initial_temperature, cooling_rate, iterations)
            print(f"Best cost found by simulated annealing with slow_time={parameter} (number {number} of {len(copied_parameters)}): {best_cost}")
            #plot_cities_and_tour(salesman.cities,salesman.optimal_route)
            #plot_weight_over_time(salesman.cities,salesman.optimal_route)

            # Store the results for plotting
            best_cost_list.append(best_cost)
            best_cost_progress_list.append(best_cost_progress)
            time_progress_list.append(time_progress)
            salary_progress_list.append(salary_progress)
            gas_progress_list.append(gas_progress)
        #plot_best_cost_progress(temperature_progress, best_cost_progress_list, squared_best_cost, copied_parameters,plot_average=True)
        average_best_cost_resid.append(np.mean(best_cost_list, axis=0))
        average_best_cost.append(np.mean(best_cost_progress_list, axis=0))   
        squared_best_cost.append(np.mean(np.square(best_cost_progress_list),axis=0)) 
        average_time_cost.append(np.mean(time_progress_list, axis=0))
        average_gas.append(np.mean(gas_progress_list, axis=0))
        average_salary.append(np.mean(salary_progress_list, axis=0))
    # Plot the best cost progress over temperature for all slow_time values
    #plot_cities_and_tour(salesman.cities,salesman.optimal_route)
    plot_over_param(dif_parameters, average_best_cost_resid)
    plot_best_cost_progress(temperature_progress, average_best_cost,  squared_best_cost, dif_parameters,plot_average=False, C_func = True)
    plot_salaries(temperature_progress, average_best_cost, average_salary, average_gas, dif_parameters)
if __name__ == "__main__":
    main()