# plotting.py
import matplotlib.pyplot as plt
import numpy as np

def plot_best_cost_progress(temperature_progress_list, best_cost_progress_list, slow_time_list, plot_average=False):
    plt.figure(figsize=(10, 5))
    for i, (slow_time, temperature_progress, best_cost_progress) in enumerate(zip(slow_time_list, temperature_progress_list, best_cost_progress_list)):
        line_style = '--' if plot_average else '-'
        color = 'black' if plot_average else f'C{i}'  # Cycle through default colors
        line_width = 1 if plot_average else 2
        label = None if plot_average else f'slow_time={slow_time}'
        plt.plot(temperature_progress, best_cost_progress, linestyle=line_style, color=color, linewidth=line_width, label=label)
        plt.title('Best Cost Progress over Temperature for Different Slowdown Factors')

    if plot_average:
        # Calculate the average best cost for each temperature progress
        average_best_cost = np.mean(best_cost_progress_list, axis=0)
        best_cost_array = np.array(best_cost_progress_list)
        squared_best_cost_array = np.square(best_cost_array)
        squared_average_best_cost = np.mean(squared_best_cost_array, axis=0)

        plt.plot(temperature_progress_list[0], average_best_cost, 'r-', linewidth=3, label='Average Best Cost')
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
    plt.yscale('log')
    plt.show()
    if plot_average:
        plot_derivation_best_cost_С(temperature_progress_list[0], average_best_cost, squared_average_best_cost)

def plot_derivation_best_cost_С(temperature_progress, average_best_cost,squared_average_best_cost):
    pass


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