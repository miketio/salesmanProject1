import math
import random
import matplotlib.pyplot as plt

class City:
    def __init__(self, x, y, package_weight):
        self.x = x
        self.y = y
        self.package_weight = package_weight

class Salesman:
    def __init__(self, cities):
        # Initialize parameters
        self.total_weight = 0.0
        self.wait_time = 1.0
        self.current_time = 9.0
        self.initial_velocity = 60
        self.hourly_salary = 200  # Example hourly salary
        self.fuel_consumption_base = 0.1  # Example fuel consumption per km (10 liters per 100 km)
        self.fuel_cost_per_liter = 50  # Example fuel cost per liter
        self.current_city = cities[0]
        self.optimal_route = cities

        # Calculate total weight of packages
        for city in cities:
            self.total_weight += city.package_weight

    def calculate_distance(self, source, destination):
        # Calculate Euclidean distance between two cities
        return math.sqrt((destination.x - source.x) ** 2 + (destination.y - source.y) ** 2)

    def calculate_base_travel_time(self, source, destination):
        # Calculate base travel time between two cities based on initial velocity
        return self.calculate_distance(source, destination) / self.initial_velocity

    def calculate_slowdown_factor(self, total_weight, cities_number):
        # Calculate slowdown factor based on total weight and number of cities
        max_weight = 3.0
        return 1.0 + 0.1 * total_weight / (max_weight * cities_number)

    def calculate_travel_time(self, source, destination, total_weight_copy, cities_number):
        # Calculate total travel time between two cities, considering slowdown and waiting time
        base_travel_time = self.calculate_base_travel_time(source, destination)
        slowdown_factor = self.calculate_slowdown_factor(total_weight_copy, cities_number)
        slowed_travel_time = base_travel_time * slowdown_factor
        return slowed_travel_time + self.wait_time

    def calculate_fuel_wasted(self, source, destination, total_weight_copy):
        return self.fuel_consuption_per_km(total_weight_copy)*self.calculate_distance(source,destination)

    def fuel_consuption_per_km(self, total_weight):
        return self.fuel_consumption_base*(1+0.001*total_weight)
    
    def calculate_total_travel_time(self):
        # Calculate the total travel time, updated current time, and remaining weight
        current_weight = self.total_weight
        current_time_copy = self.current_time
        total_travel_time = 0.0
        fuel_wasted = 0.0

        for i in range(len(self.optimal_route)):
            city = self.optimal_route[i]
            next_city = self.optimal_route[(i + 1) % len(self.optimal_route)]
            cities_number = len(self.optimal_route)
            total_travel_time += self.calculate_travel_time(city, next_city, current_weight, cities_number)
            current_time_copy += total_travel_time
            current_time_copy = current_time_copy % 24.0
            current_weight -= next_city.package_weight
            fuel_wasted += self.calculate_fuel_wasted(city, next_city, current_weight)
        return total_travel_time, current_time_copy, fuel_wasted
    
    def calculate_total_cost(self):
        # Calculate the total cost, considering both hourly salary and fuel cost
        total_travel_time, _, fuel_wasted = self.calculate_total_travel_time()
        return total_travel_time * self.hourly_salary + fuel_wasted*self.fuel_cost_per_liter

    def simulated_annealing_tsp(self, initial_temperature, iterations):
        # Simulated annealing optimization algorithm for the traveling salesman problem
        best_salesman = Salesman(self.optimal_route.copy())
        best_total_cost = self.calculate_total_cost()

        temperature = initial_temperature

        for _ in range(iterations):
            new_salesman = Salesman(self.optimal_route.copy())
            city_index1 = random.randint(0, len(self.optimal_route) - 1)
            city_index2 = random.randint(0, len(self.optimal_route) - 1)
            new_salesman.optimal_route[city_index1], new_salesman.optimal_route[city_index2] = (
                new_salesman.optimal_route[city_index2],
                new_salesman.optimal_route[city_index1],
            )

            delta_h = new_salesman.calculate_total_cost() - self.calculate_total_cost()

            if delta_h < 0 or random.random() < math.exp(-delta_h / temperature):
                self.optimal_route = new_salesman.optimal_route[:]

            if self.calculate_total_cost() < best_total_cost:
                best_salesman.optimal_route = self.optimal_route[:]
                best_total_cost = self.calculate_total_cost()

            temperature *= 0.99

        self.optimal_route = best_salesman.optimal_route[:]

# Function to plot cities and tour
def plot_cities_and_tour(cities, tour):
    city_x = [city.x for city in cities]
    city_y = [city.y for city in cities]

    tour_x = [city.x for city in tour]
    tour_y = [city.y for city in tour]

    plt.plot(city_x, city_y, 'ro', label='Cities')
    plt.plot(tour_x + [tour_x[0]], tour_y + [tour_y[0]], 'b-', label='Best Tour')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Create a list of cities
    cities = [
        City(13, 4, 2.0),  City(32, 68, 1.5), City(87, 54, 2.5), City(45, 32, 2.0), City(67, 89, 3.0),
        City(23, 11, 1.0), City(78, 98, 2.5), City(56, 23, 1.5), City(34, 76, 2.0), City(90, 12, 1.0),
        City(45, 67, 2.5), City(23, 87, 1.5), City(76, 34, 2.0), City(11, 23, 1.0), City(98, 45, 3.0),
        City(32, 56, 1.5), City(68, 90, 2.0), City(4, 13, 1.0), City(54, 87, 2.5), City(89, 45, 1.5)
    ]

    # Set the number of iterations for simulated annealing
    sa_iterations = 15000

    # Create a salesman object
    salesman = Salesman(cities)

    # Run simulated annealing to optimize the tour
    salesman.simulated_annealing_tsp(100.0, sa_iterations)

    # Print the results
    best_total_cost = salesman.calculate_total_cost()
    print(f"\nTotal Cost: rub {best_total_cost:.2f}")

    # Plot the cities and the best tour
    print("Best TSP Tour with Timestamps:")
    current_weight = salesman.total_weight
    current_time_copy = salesman.current_time
    total_travel_time = 0.0
    for i in range(len(salesman.optimal_route)):
        city = salesman.optimal_route[i]
        next_city = salesman.optimal_route[(i + 1) % len(salesman.optimal_route)]

        print(f"({city.x}, {city.y}) ", end='')
        travel_time = salesman.calculate_travel_time(city, next_city,current_weight, len(salesman.optimal_route))
        current_time_copy += travel_time
        current_time_copy = current_time_copy % 24.0
        current_weight -= next_city.package_weight
        current_weight = max(current_weight,0)
        print(f"{current_time_copy:.2f} hours", end='')
    plot_cities_and_tour(cities, salesman.optimal_route)