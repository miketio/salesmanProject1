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
    plt.show()
    if plot_average:
        #plot_derivation_best_cost_С(temperature_progress_list[0], average_best_cost)
        plot_average_best_cost_derivative(np.log(temperature_progress_list[0]), average_best_cost, process_variance=1e-5, measurement_variance=0.8)
 

def kalman_filter(data, process_variance, measurement_variance):
    # Initial state estimation (can be set based on prior knowledge)
    x_est = data[0]
    
    # Initial estimation covariance
    P_est = 1
    
    # Kalman gain
    K = 0
    
    # Filtered data
    filtered_data = []
    
    for measurement in data:
        # Prediction step
        x_pred = x_est
        P_pred = P_est + process_variance
        
        # Update step
        K = P_pred / (P_pred + measurement_variance)
        x_est = x_pred + K * (measurement - x_pred)
        P_est = (1 - K) * P_pred
        
        filtered_data.append(x_est)
    
    return np.array(filtered_data)

def plot_average_best_cost_derivative(temperature_progress, average_best_cost, process_variance=0.01, measurement_variance=0.1):
    # Apply Kalman filter to smooth the data
    smoothed_average_best_cost = kalman_filter(average_best_cost, process_variance, measurement_variance)
    
    # Calculate the derivative of the smoothed average best cost
    derivative_average_best_cost = np.gradient(smoothed_average_best_cost, temperature_progress)
    
    # Plot the derivative of the smoothed average best cost
    plt.figure(figsize=(10, 5))
    plt.plot(np.exp(temperature_progress), derivative_average_best_cost, 'g-', linewidth=2, label='Derivative of Smoothed Average Best Cost')
    plt.xlabel('Temperature Progress')
    plt.ylabel('Derivative')
    plt.title('Derivative of Smoothed Average Best Cost (Kalman Filter)')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.xlim(np.exp(-10),np.exp(20))
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