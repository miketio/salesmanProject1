# plotting.py
import matplotlib.pyplot as plt
import numpy as np

def plot_best_cost_progress(temperature_progress_list, best_cost_progress_list, slow_time_list):
    plt.figure(figsize=(10, 5))
    for slow_time, temperature_progress, best_cost_progress in zip(slow_time_list, temperature_progress_list, best_cost_progress_list):
        plt.plot(temperature_progress, best_cost_progress, label=f'slow_time={slow_time}')
    plt.xlabel('Temperature')
    plt.ylabel('Best Cost')
    plt.title('Best Cost Progress over Temperature for Different Slowdown Factors')
    plt.legend()
    plt.grid(True)
    # Set the x-axis and y-axis to logarithmic scale
    plt.xscale('log')
    plt.yscale('log')
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