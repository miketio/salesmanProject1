# MCmethods.py
import random
import math

def random_walk(salesman, iterations):
    for _ in range(iterations):
        city_index1, city_index2 = random.sample(range(salesman.num_cities), 2)
        new_route = salesman.optimal_route[:]
        new_route[city_index1], new_route[city_index2] = new_route[city_index2], new_route[city_index1]
        current_total_cost = salesman.calculate_total_cost(salesman.optimal_route)
        new_total_cost = salesman.calculate_total_cost(new_route)
        acceptance_probability = min(1, math.exp((current_total_cost - new_total_cost)))
        if random.random() < acceptance_probability:
            salesman.optimal_route = new_route
    best_total_cost = salesman.calculate_total_cost()
    return best_total_cost

def simulated_annealing(salesman, initial_temperature, cooling_rate, iterations):
    best_salesman = salesman.__class__(salesman.optimal_route)
    best_total_cost = salesman.calculate_total_cost()
    salary = salesman.calculate_separated_cost()[0]
    gas = salesman.calculate_separated_cost()[1]
    temperature = initial_temperature
    temperature_progress = []
    best_total_cost_progress = []# add here a massive of best_total_cost(temperature) in simulated annealing method
    time_progress = []
    salary_progress = []
    gas_progress = []
    for _ in range(iterations):
        new_salesman = salesman.__class__(salesman.optimal_route)
        city_index1 = random.randint(0, salesman.num_cities - 1)
        city_index2 = random.randint(0, salesman.num_cities - 1)
        new_salesman.optimal_route[city_index1], new_salesman.optimal_route[city_index2] = (
            new_salesman.optimal_route[city_index2],
            new_salesman.optimal_route[city_index1],
        )
        delta_h = new_salesman.calculate_total_cost() - salesman.calculate_total_cost()

        if delta_h < 0 or random.random() < math.exp(-delta_h / temperature):
            salesman.optimal_route = new_salesman.optimal_route

        if salesman.calculate_total_cost() < best_total_cost:
            best_salesman.optimal_route = salesman.optimal_route
            best_total_cost = salesman.calculate_total_cost()
            gas = salesman.calculate_separated_cost()[1]
            salary = salesman.calculate_separated_cost()[0]

        best_total_cost_progress.append(best_total_cost)
        salary_progress.append(salary)
        gas_progress.append(gas)
        temperature_progress.append(temperature)
        temperature *= (1 - cooling_rate)
        time_progress.append(salesman.calculate_total_travel_time()[0])
    salesman.optimal_route = best_salesman.optimal_route
    return best_total_cost, best_total_cost_progress, temperature_progress, time_progress, salary_progress, gas_progress