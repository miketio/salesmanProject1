#math functions
import numpy as np

def gaussian_function(x):
    mu1 = 8
    sigma1 = 0.75
    mu2 = 17
    sigma2 = 1
    # Gaussian function for the first distribution
    gaussian1 = 1 / (sigma1 * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu1) / sigma1) ** 2)
    # Gaussian function for the second distribution
    gaussian2 = 1 / (sigma2 * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu2) / sigma2) ** 2)
    # Return the sum of the two Gaussian functions
    return 1*gaussian1 + 2*gaussian2


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
