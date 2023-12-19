#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <ctime>

// Gnuplot headers
#include "gnuplot-iostream.h"

using namespace std;

// Structure to represent a city with x and y coordinates
struct City {
    int x, y;

    City(int x, int y) : x(x), y(y) {}
};

// Structure to represent a road between two cities
struct Road {
    double difficulty; // Difficulty factor (affected by traffic, time of day, etc.)
    double distance;   // Distance between cities

    Road(double difficulty, double distance) : difficulty(difficulty), distance(distance) {}
};

// Function to calculate the difficulty factor based on time
double calculateDifficulty(double time) {
    return 1 + 2 * exp(-pow((time - 18) / 0.5, 2));
}

// Function to calculate the Euclidean distance between two cities
double calculateDistance(const City& city1, const City& city2) {
    return sqrt(pow(city1.x - city2.x, 2) + pow(city1.y - city2.y, 2));
}

// Function to calculate the travel time between two cities
double calculateTravelTime(const City& city1, const City& city2, double currentTime) {
    double roadDifficulty = calculateDifficulty(currentTime);
    double distance = calculateDistance(city1, city2);

    // Assuming a base speed of 60 km/h (adjust as needed)
    double baseSpeed = 60.0;
    double travelTime = distance / (baseSpeed * (1.0 + roadDifficulty));
    return travelTime;
}

// Function to calculate the total travel time of a tour
double calculateTotalTravelTime(const vector<City>& tour, double currentTime) {
    double totalTravelTime = 0.0;

    for (size_t i = 0; i < tour.size() - 1; ++i) {
        const City& currentCity = tour[i];
        const City& nextCity = tour[i + 1];

        // Calculate travel time between cities
        double travelTime = calculateTravelTime(currentCity, nextCity, currentTime);

        // Assuming a fixed waiting time in each city (adjust as needed)
        double waitTimePerCity = 1.0;

        // Add travel time and wait time in each city
        totalTravelTime += travelTime + waitTimePerCity;

        // Update current time for the next leg of the tour
        currentTime += travelTime + waitTimePerCity;
    }

    // Add travel time for the last leg of the tour
    totalTravelTime += calculateTravelTime(tour.back(), tour.front(), currentTime);

    return totalTravelTime;
}

// Function to perform Simulated Annealing optimization for TSP with time constraints
vector<City> simulatedAnnealingTSP(const vector<City>& cities, double initialTemperature, int iterations, double currentTime) {
    // Initialize the current solution with a random permutation of cities
    vector<City> currentSolution = cities;
    random_shuffle(currentSolution.begin(), currentSolution.end());

    // Initialize the best solution
    vector<City> bestSolution = currentSolution;

    // Initialize the current travel time
    double currentTravelTime = calculateTotalTravelTime(currentSolution, currentTime);

    // Initialize the best travel time
    double bestTravelTime = currentTravelTime;

    // Initialize the current temperature
    double temperature = initialTemperature;

    // Perform Simulated Annealing iterations
    for (int iter = 0; iter < iterations; ++iter) {
        // Generate a new solution by swapping two random cities
        vector<City> newSolution = currentSolution;
        int cityIndex1 = rand() % cities.size();
        int cityIndex2 = rand() % cities.size();
        swap(newSolution[cityIndex1], newSolution[cityIndex2]);

        // Calculate the change in travel time
        double deltaH = calculateTotalTravelTime(newSolution, currentTime) - currentTravelTime;

        // Accept the new solution with a probability based on the acceptance criterion
        if (deltaH < 0 || (rand() / static_cast<double>(RAND_MAX)) < exp(-deltaH / temperature)) {
            currentSolution = newSolution;
            currentTravelTime = calculateTotalTravelTime(currentSolution, currentTime);
        }

        // Update the best solution if needed
        if (currentTravelTime < bestTravelTime) {
            bestSolution = currentSolution;
            bestTravelTime = currentTravelTime;
        }

        // Update the temperature (annealing schedule)
        temperature *= 0.99;  // Adjust the cooling factor as needed
    }

    return bestSolution;
}
// Function to plot cities and the tour using Gnuplot
void plotCitiesAndTour(const vector<City>& cities, const vector<City>& tour) {
    Gnuplot gp;

    // Plot cities with larger red points and coordinates
    gp << "plot '-' with points pt 7 ps 2 lc rgb 'red' title 'Cities', '-' with lines title 'Best Tour'\n";

    for (const auto& city : cities) {
        gp << city.x << " " << city.y << "\n";
    }
    gp << "e\n";

    for (const auto& city : tour) {
        gp << city.x << " " << city.y << "\n";
    }
    gp << tour.front().x << " " << tour.front().y << "\n"; // Close the loop
    gp << "e\n";

    gp.flush();
}

int main() {
    // Seed for random number generation
    srand(static_cast<unsigned int>(time(nullptr)));

    // Create a set of 20 predefined cities
    vector<City> cities = {
        {13, 4}, {32, 68}, {87, 54}, {45, 32}, {67, 89},
        {23, 11}, {78, 98}, {56, 23}, {34, 76}, {90, 12},
        {45, 67}, {23, 87}, {76, 34}, {11, 23}, {98, 45},
        {32, 56}, {68, 90}, {4, 13}, {54, 87}, {89, 45}
    };

    // Number of Simulated Annealing iterations
    int saIterations = 5000;

    // Current time when the salesman starts the journey (in 24-hour format)
    double currentTime = 9.0; // Starting at 9:00 AM

    // Perform Simulated Annealing optimization
    vector<City> bestTour = simulatedAnnealingTSP(cities, 100.0, saIterations, currentTime);

    // Output the best tour
    cout << "Best TSP Tour: ";
    for (const auto& city : bestTour) {
        cout << "(" << city.x << ", " << city.y << ") ";
    }

    cout << "Best TSP Tour with Timestamps: ";
    for (size_t i = 0; i < bestTour.size(); ++i) {
        const auto& city = bestTour[i];
        cout << "(" << city.x << ", " << city.y << ") ";

        // Output timestamp for each city
        double travelTime = calculateTravelTime(city, bestTour[(i + 1) % bestTour.size()], currentTime) + 1.0;
        currentTime += travelTime;
        currentTime = fmod(currentTime, 24.0); // Ensure the time is within a 24-hour cycle
        cout << "@" << currentTime << " ";
    }

    // Output the total travel time of the best tour
    double bestTravelTime = calculateTotalTravelTime(bestTour, 9.0);
    cout << "\nTotal Travel Time: " << bestTravelTime << " hours" << endl;

    // Plot cities and the best tour with timestamps
    plotCitiesAndTour(cities, bestTour);

    return 0;
}
