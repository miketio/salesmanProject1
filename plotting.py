# plotting.py
import matplotlib.pyplot as plt
import numpy as np
from math_functions import kalman_filter, gaussian_function

def plot_best_cost_progress(temperature_progress, best_cost_progress_list, squared_best_cost, slow_time_list, plot_average=False, C_func = False):
    if plot_average:
        fig = plt.figure(figsize=(10, 5))
        ax1 = fig.add_subplot(1, 2, 1)
        line_style = '--'
        color = 'black'
        line_width = 1
        label = None
        # Calculate the average best cost for each temperature progress
        average_best_cost = np.mean(best_cost_progress_list, axis=0)
        for best_cost in best_cost_progress_list:
            ax1.plot(temperature_progress,best_cost, line_style, color = color,linewidth=line_width, label = label)
        ax1.plot(temperature_progress, average_best_cost, 'r-', linewidth=3, label='Average C$_{total}$')
        ax1.legend(loc='best')
        # Add a legend for the dashed lines
        ax1.plot([], [], 'k--', label='Single solution (one at a time)')
        ax1.legend(loc='best')
        ax1.set_xlabel('Temperature')
        ax1.set_ylabel('C$_{total}$', fontsize=12)
        ax1.legend()
        ax1.grid(True)
        # Set the x-axis and y-axis to logarithmic scale
        ax1.set_xscale('log')
        smoothed_average_best_cost = kalman_filter(average_best_cost, process_variance=1e-5, measurement_variance=0.1)
        
        # Calculate the derivative of the smoothed average best cost
        derivative_average_best_cost = np.gradient(smoothed_average_best_cost, np.log(temperature_progress))
        
        # Plot the derivative of the smoothed average best cost
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.plot(np.exp(temperature_progress)[30:], derivative_average_best_cost[30:], 'g-', linewidth=2, label='Derivative of Smoothed Average Best Cost')
        ax2.set_xlabel('Temperature')
        ax2.set_ylabel('Derivative')
        ax2.set_title('Derivative of Smoothed Average Best Cost')
        ax2.legend()
        ax2.grid(True)
        ax2.set_xscale('log')
        ax2.set_xlim(np.exp(-15),np.exp(20))
        ax2.set_ylim(0,2000)
        plt.show()

    else:
        fig = plt.figure(figsize=(15, 5))
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)
        for i, (slow_time, best_cost_progress, squared_progress) in enumerate(zip(slow_time_list, best_cost_progress_list,squared_best_cost)):
            line_style = '-'
            color = f'C{i}'  # Cycle through default colors
            line_width = 2
            label = f'initial velocity ={slow_time}'            
            ax1.plot(temperature_progress, best_cost_progress, linestyle=line_style, color=color, linewidth=line_width, label=label)
            #ax1.set_title('Best Cost Progress over Temperature for Different Slowdown Factors')
            ax1.set_xlabel('Temperature')
            ax1.set_ylabel('C$_{total}$', fontsize=12)
            ax1.set_xscale('log')
            ax1.legend()
            ax1.grid(True)
            ax1.set_xlim(np.exp(-15),np.exp(20))

            smoothed_average_best_cost = kalman_filter(best_cost_progress, process_variance=1e-5, measurement_variance=0.1)
            derivative_average_best_cost = np.gradient(smoothed_average_best_cost, np.log(temperature_progress))
            ax2.plot((temperature_progress)[30:], derivative_average_best_cost[30:], linestyle=line_style, color=color, linewidth=line_width, label=label)
            ax2.set_xlabel('Temperature')
            ax2.set_ylabel('Derivative')
            #ax2.set_title('Derivative of Smoothed Average Best Cost')
            ax2.legend()
            ax2.grid(True)
            ax2.set_xscale('log')
            ax2.set_xlim(np.exp(-15),np.exp(20))
            ax2.set_ylim(0,2000)

            variance = kalman_filter(squared_progress - np.square(best_cost_progress), process_variance=0.01, measurement_variance=0.1)#/np.square(temperature_progress)
            ax3.plot(temperature_progress, variance, linestyle=line_style, color=color, linewidth=line_width, label=label)
            #ax3.set_title('Variance')
            ax3.set_xlabel('Temperature')
            ax3.set_ylabel('Variance')
            plt.legend()
            plt.grid(True)
            ax3.set_xscale('log')
            ax3.set_xlim(np.exp(-15),np.exp(20))
        plt.show()


def plot_average_best_cost_derivative(temperature_progress, average_best_cost, process_variance=0.01, measurement_variance=0.1):
    # Apply Kalman filter to smooth the data
    smoothed_average_best_cost = kalman_filter(average_best_cost, process_variance, measurement_variance)
    
    # Calculate the derivative of the smoothed average best cost
    derivative_average_best_cost = np.gradient(smoothed_average_best_cost, temperature_progress)
    
    # Plot the derivative of the smoothed average best cost
    plt.figure(figsize=(10, 5))
    plt.plot(np.exp(temperature_progress)[30:], derivative_average_best_cost[30:], 'g-', linewidth=2, label='Derivative of Smoothed Average Best Cost')
    plt.xlabel('Temperature Progress')
    plt.ylabel('Derivative')
    plt.title('Derivative of Smoothed Average Best Cost')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.xlim(np.exp(-15),np.exp(20))
    plt.ylim(0,2000)
    plt.show()

def plot_cities_and_tour(cities, tour):
    x_coords = [city.x for city in cities]
    y_coords = [city.y for city in cities]
    plt.scatter(x_coords, y_coords, color='blue')

    # Connect the cities in the tour with lines
    for i in range(len(tour)):
        current_city = tour[i]
        next_city = tour[(i + 1) % len(tour)]
        plt.plot([current_city.x, next_city.x], [current_city.y, next_city.y], color='red')

    plt.title('Cities and Tour')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()

def plot_gaussian_function(start=0, end=24, num_points=1000):
    # Generate x values
    x = np.linspace(start, end, num_points)
    # Calculate y values
    y = gaussian_function(x)
    
    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label='Trafic function')
    plt.xlabel('Time, hours')
    plt.ylabel('η$_{time}$', fontsize=12)
    plt.title('η$_{time}$ over time')
    plt.legend()
    plt.grid(True)
    plt.xlim(0,24)
    plt.show()

def plot_weight_over_time(salesman):

    current_weight = salesman.total_weight
    current_time_copy = salesman.current_time
    total_travel_time = 0.0
    time_array = [current_weight]
    weight_array = [current_time_copy]
    fuel_wasted = 0.0
    route = salesman.optimal_route
    for i in range(len(route)):
        city = route[i]
        next_city = route[(i + 1) % salesman.num_cities]
        total_travel_time += salesman.calculate_travel_time(city, next_city, salesman.calculate_slowdown_factor(current_time_copy))
        
        current_time_copy += total_travel_time
        current_time_copy = current_time_copy % 24.0
        current_weight -= next_city.package_weight
        time_array.append(current_time_copy)
        weight_array.append(current_weight)
        fuel_wasted += salesman.calculate_fuel_wasted(city, next_city)
    plt.plot(time_array,weight_array)
    
#plot_gaussian_function()
def plot_salaries(temperature_progress, total_cost_list, salary_list, gas_list, slow_time_list):
    fig = plt.figure(figsize=(15, 5))
    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1, 3, 3)
    for i, (slow_time, best_cost_progress, salary, gas) in enumerate(zip(slow_time_list, total_cost_list, salary_list, gas_list)):
        line_style = '-'
        color = f'C{i}'  # Cycle through default colors
        line_width = 2
        label = f'initial velocity ={slow_time}' 

        ax1.plot(temperature_progress, best_cost_progress, linestyle=line_style, color=color, linewidth=line_width, label=label)
        #ax1.set_title('Best Cost Progress over Temperature for Different Slowdown Factors')
        ax1.set_xlabel('Temperature')
        ax1.set_ylabel('C$_{total}$', fontsize=12)
        ax1.set_xscale('log')
        ax1.legend()
        ax1.grid(True)
        ax1.set_xlim(np.exp(-15),np.exp(20))

        ax2.plot(temperature_progress, salary, linestyle=line_style, color=color, linewidth=line_width, label=label)
        #ax1.set_title('Best Cost Progress over Temperature for Different Slowdown Factors')
        ax2.set_xlabel('Temperature')
        ax2.set_ylabel('Salary', fontsize=12)
        ax2.set_xscale('log')
        ax2.legend()
        ax2.grid(True)
        ax2.set_xlim(np.exp(-15),np.exp(20))

        ax3.plot(temperature_progress, gas, linestyle=line_style, color=color, linewidth=line_width, label=label)
        #ax1.set_title('Best Cost Progress over Temperature for Different Slowdown Factors')
        ax3.set_xlabel('Temperature')
        ax3.set_ylabel('Gas', fontsize=12)
        ax3.set_xscale('log')
        ax3.legend()
        ax3.grid(True)
        ax3.set_xlim(np.exp(-15),np.exp(20))
    plt.show()