#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>

class City {
public:
    double x, y, package_weight;

    City(double x, double y, double package_weight) : x(x), y(y), package_weight(package_weight) {}
};

class Salesman {
public:
    double total_weight, wait_time, current_time, initial_velocity, hourly_salary, fuel_consumption_base, fuel_cost_per_liter;
    std::vector<City> current_city, optimal_route;

    Salesman(std::vector<City>& cities)
        : total_weight(0.0), wait_time(1.0), current_time(9.0), initial_velocity(60),
          hourly_salary(200), fuel_consumption_base(0.1), fuel_cost_per_liter(50), optimal_route(cities) {

        // Calculate total weight of packages
        for (const auto& city : cities) {
            total_weight += city.package_weight;
        }
    }

    double calculate_distance(const City& source, const City& destination) {
        // Calculate Euclidean distance between two cities
        return std::sqrt(std::pow(destination.x - source.x, 2) + std::pow(destination.y - source.y, 2));
    }

    double calculate_base_travel_time(const City& source, const City& destination) {
        // Calculate base travel time between two cities based on initial velocity
        return calculate_distance(source, destination) / initial_velocity;
    }

    double calculate_slowdown_factor(double total_weight, int cities_number) {
        // Calculate slowdown factor based on total weight and number of cities
        double max_weight = 3.0;
        return 1.0 + 0.1 * total_weight / (max_weight * cities_number);
    }

    double calculate_travel_time(const City& source, const City& destination, double total_weight_copy, int cities_number) {
        // Calculate total travel time between two cities, considering slowdown and waiting time
        double base_travel_time = calculate_base_travel_time(source, destination);
        double slowdown_factor = calculate_slowdown_factor(total_weight_copy, cities_number);
        double slowed_travel_time = base_travel_time * slowdown_factor;
        return slowed_travel_time + wait_time;
    }

    double calculate_fuel_wasted(const City& source, const City& destination, double total_weight_copy) {
        return fuel_consuption_per_km(total_weight_copy) * calculate_distance(source, destination);
    }

    double fuel_consuption_per_km(double total_weight) {
        return fuel_consumption_base * (1 + 0.001 * total_weight);
    }

    std::tuple<double, double, double> calculate_total_travel_time() {
        // Calculate the total travel time, updated current time, and remaining weight
        double current_weight = total_weight;
        double current_time_copy = current_time;
        double total_travel_time = 0.0;
        double fuel_wasted = 0.0;

        for (size_t i = 0; i < optimal_route.size(); ++i) {
            const auto& city = optimal_route[i];
            const auto& next_city = optimal_route[(i + 1) % optimal_route.size()];
            int cities_number = optimal_route.size();

            total_travel_time += calculate_travel_time(city, next_city, current_weight, cities_number);
            current_time_copy += total_travel_time;
            current_time_copy = std::fmod(current_time_copy, 24.0);
            current_weight -= next_city.package_weight;
            fuel_wasted += calculate_fuel_wasted(city, next_city, current_weight);
        }

        return std::make_tuple(total_travel_time, current_time_copy, fuel_wasted);
    }

    double calculate_total_cost() {
        // Calculate the total cost, considering both hourly salary and fuel cost
        auto [total_travel_time, _, fuel_wasted] = calculate_total_travel_time();
        return total_travel_time * hourly_salary + fuel_wasted * fuel_cost_per_liter;
    }

    void simulated_annealing_tsp(double initial_temperature, int iterations) {
        // Simulated annealing optimization algorithm for the traveling salesman problem
        Salesman best_salesman = *this;
        double best_total_cost = calculate_total_cost();
        double temperature = initial_temperature;

        for (int i = 0; i < iterations; ++i) {
            Salesman new_salesman = *this;
            int city_index1 = rand() % optimal_route.size();
            int city_index2 = rand() % optimal_route.size();
            std::swap(new_salesman.optimal_route[city_index1], new_salesman.optimal_route[city_index2]);

            double delta_h = new_salesman.calculate_total_cost() - calculate_total_cost();

            if (delta_h < 0 || (rand() / static_cast<double>(RAND_MAX)) < std::exp(-delta_h / temperature)) {
                optimal_route = new_salesman.optimal_route;
            }

            if (calculate_total_cost() < best_total_cost) {
                best_salesman.optimal_route = optimal_route;
                best_total_cost = calculate_total_cost();
            }

            temperature *= 0.99;
        }

        optimal_route = best_salesman.optimal_route;
    }
};

// Function to plot cities and tour (not implemented in C++)
void plot_cities_and_tour(const std::vector<City>& cities, const std::vector<City>& tour) {
    // Implementation depends on the graphics library used in C++
}

int main() {
    // Create a list of cities
    std::vector<City> cities = {
        {13, 4, 2.0},  {32, 68, 1.5}, {87, 54, 2.5}, {45, 32, 2.0}, {67, 89, 3.0},
        {23, 11, 1.0}, {78, 98, 2.5}, {56, 23, 1.5}, {34, 76, 2.0}, {90, 12, 1.0},
        {45, 67, 2.5}, {23, 87, 1.5}, {76, 34, 2.0}, {11, 23, 1.0}, {98, 45, 3.0},
        {32, 56, 1.5}, {68, 90, 2.0}, {4, 13, 1.0}, {54, 87, 2.5}, {89, 45, 1.5}
    };

    // Set the number of iterations for simulated annealing
    int sa_iterations = 15000;

    // Create a salesman object
    Salesman salesman(cities);

    // Run simulated annealing to optimize the tour
    salesman.simulated_annealing_tsp(100.0, sa_iterations);

    // Print the results
    double best_total_cost = salesman.calculate_total_cost();
    std::cout << "\nTotal Cost: rub " << best_total_cost << ".2f" << std::endl;

    // Plot the cities and the best tour (not implemented in C++)
    std::cout << "Best TSP Tour with Timestamps:" << std::endl;
    double current_weight = salesman.total_weight;
    double current_time_copy = salesman.current_time;
    double total_travel_time = 0.0;

    for (size_t i = 0; i < salesman.optimal_route.size(); ++i) {
        const auto& city = salesman.optimal_route[i];
        const auto& next_city = salesman.optimal_route[(i + 1) % salesman.optimal_route.size()];

        std::cout << "(" << city.x << ", " << city.y << ") ";
        double travel_time = salesman.calculate_travel_time(city, next_city, current_weight, salesman.optimal_route.size());
        current_time_copy += travel_time;
        current_time_copy = std::fmod(current_time_copy, 24.0);
        current_weight -= next_city.package_weight;
        current_weight = std::max(current_weight, 0.0);
        std::cout << current_time_copy << " hours" << std::endl;
        std::cout << current_weight << " kilos" << std::endl;
    }

    // The plot_cities_and_tour function is not implemented in C++
    // plot_cities_and_tour(cities, salesman.optimal_route);

    return 0;
}