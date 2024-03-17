# plotting.py
import matplotlib.pyplot as plt
import numpy as np
from math_functions import kalman_filter, gaussian_function

def plot_best_cost_progress(temperature_progress, best_cost_progress_list, slow_time_list, plot_average=False):
    plt.figure(figsize=(10, 5))
    for i, (slow_time, best_cost_progress) in enumerate(zip(slow_time_list, best_cost_progress_list)):
        line_style = '--' if plot_average else '-'
        color = 'black' if plot_average else f'C{i}'  # Cycle through default colors
        line_width = 1 if plot_average else 2
        label = None if plot_average else f'slow_time={slow_time}'
        plt.plot(temperature_progress, best_cost_progress, linestyle=line_style, color=color, linewidth=line_width, label=label)
        plt.title('Best Cost Progress over Temperature for Different Slowdown Factors')

    if plot_average:
        # Calculate the average best cost for each temperature progress
        average_best_cost = np.mean(best_cost_progress_list, axis=0)
        plt.plot(temperature_progress, average_best_cost, 'r-', linewidth=3, label='Average Best Cost')
        plt.legend(loc='best')
        # Add a legend for the dashed lines
        plt.plot([], [], 'k--', label='Single solution (one at a time)')
        plt.legend(loc='best')
        plt.title('Average Best Cost over Temperature')
        
    plt.xlabel('Temperature')
    plt.ylabel('Best Cost')
    
    plt.legend()
    plt.grid(True)
    # Set the x-axis and y-axis to logarithmic scale
    plt.xscale('log')
    plt.show()
    if plot_average:
        plot_average_best_cost_derivative(np.log(temperature_progress), average_best_cost, process_variance=1e-5, measurement_variance=0.8)

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
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Sum of Two Gaussian Functions')
    plt.legend()
    plt.grid(True)
    plt.show()

#plot_gaussian_function()