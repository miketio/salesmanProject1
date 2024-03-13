# salesman.py
import random
import math
import numpy as np
from city import City
from MCmethods import simulated_annealing, metropolis_hastings
from math_functions import gaussian_function

class Salesman:
    def __init__(self, cities):
        # Initialize parameters
        self.cities = cities
        self.total_weight = sum(city.package_weight for city in cities)
        self.max_weight = self.total_weight
        self.wait_time = 1.0
        self.current_time = 9.0
        self.initial_velocity = 60
        self.hourly_salary = 200  # Example hourly salary
        self.fuel_consumption_base = 0.1  # Example fuel consumption per km (10 liters per 100 km)
        self.fuel_cost_per_liter = 50  # Example fuel cost per liter
        self.current_city = cities[0]
        self.optimal_route = cities[:]  # Make a copy of the cities list
        self.num_cities = len(cities)
        self.distance_matrix = self._create_distance_matrix()
        self.slow_time = 1
        self.slow_weight = 0.1

    def _create_distance_matrix(self):
        # Create a matrix to store distances between cities
        distance_matrix = {}
        for i, city1 in enumerate(self.cities):
            for j, city2 in enumerate(self.cities):
                if i != j:
                    distance_matrix[(i, j)] = city1.distance_to(city2)
        return distance_matrix

    def calculate_distance(self, city1, city2):
        # Retrieve the distance from the distance matrix if it exists
        if (self.cities.index(city1), self.cities.index(city2)) in self.distance_matrix:
            return self.distance_matrix[(self.cities.index(city1), self.cities.index(city2))]
        elif (self.cities.index(city2), self.cities.index(city1)) in self.distance_matrix:
            return self.distance_matrix[(self.cities.index(city2), self.cities.index(city1))]
        # Otherwise, calculate the distance and store it in the matrix
        distance = math.sqrt((city2.x - city1.x) ** 2 + (city2.y - city1.y) ** 2)
        self.distance_matrix[(self.cities.index(city1), self.cities.index(city2))] = distance
        return distance

    def calculate_base_travel_time(self, city1, city2):
        # Calculate base travel time between two cities based on initial velocity
        return self.calculate_distance(city1, city2) / self.initial_velocity

    def calculate_slowdown_factor(self,time):
        # Calculate slowdown factor based on total weight and the current time
        return 1 + gaussian_function(time)*self.slow_time +(self.total_weight / self.max_weight) *self.slow_weight

    def calculate_travel_time(self, city1, city2, slowdown_factor):
        # Calculate total travel time between two cities, considering slowdown and waiting time
        base_travel_time = self.calculate_base_travel_time(city1, city2)
        slowed_travel_time = base_travel_time * slowdown_factor
        return slowed_travel_time + self.wait_time

    def calculate_fuel_wasted(self, city1, city2):
        return self.fuel_consumption_per_km() * self.calculate_distance(city1, city2)

    def fuel_consumption_per_km(self):
        return self.fuel_consumption_base * (1 + 0.001 * self.total_weight)

    def calculate_total_cost(self, route=None):
        # Calculate the total cost of a given route
        if route is None:
            route = self.optimal_route
        total_travel_time, _, fuel_wasted = self.calculate_total_travel_time(route)
        return total_travel_time * self.hourly_salary + fuel_wasted * self.fuel_cost_per_liter

    def calculate_total_travel_time(self, route=None):
        # Calculate the total travel time for a given route
        if route is None:
            route = self.optimal_route
        current_weight = self.total_weight
        current_time_copy = self.current_time
        total_travel_time = 0.0
        fuel_wasted = 0.0

        for i in range(len(route)):
            city = route[i]
            next_city = route[(i + 1) % self.num_cities]
            total_travel_time += self.calculate_travel_time(city, next_city, self.calculate_slowdown_factor(current_time_copy))
            current_time_copy += total_travel_time
            current_time_copy = current_time_copy % 24.0
            current_weight -= next_city.package_weight
            fuel_wasted += self.calculate_fuel_wasted(city, next_city)
        return total_travel_time, current_time_copy, fuel_wasted

    def simulated_annealing(self, initial_temperature, cooling_rate, iterations):
        return simulated_annealing(self, initial_temperature, cooling_rate, iterations)


    def metropolis_hastings(self, iterations):
        return metropolis_hastings(self, iterations)