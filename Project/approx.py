"""
This code implemented the generalized greedy algorithm to approximate the knapsack problem
In addition to normal parameters(values, weights, capacity), this algorithm require a \epsilon to adjust the size of the greedy subset.
The algorithm is describe in this paper:
https://www3.cs.stonybrook.edu/~keriko/approx.pdf
"""

import os
import time
from itertools import combinations

# Defines an Approx class for solving the Knapsack problem using an approximation algorithm
class Approx:
    def __init__(self, cutoff_time, filePath):
        self.cut_off = cutoff_time  # Maximum time limit (in seconds) for the algorithm to run
        self.filePath = filePath  # Path to the input file

    # Executes the approximation algorithm
    def run_Approx(self, capacity, values, weights, epsilon):
        self.start_time = time.time()  # Records the start time of the algorithm
        n = len(values)  # Number of items

        # Creates a list containing each item's index, value, weight, and the ratio of value to weight, sorted by ratio in descending order
        index_value_weight_ratio = [(index, value, weight, value / weight) for index, (value, weight) in enumerate(zip(values, weights))]
        index_value_weight_ratio.sort(key=lambda x: x[3], reverse=True)

        total_weight = 0
        total_value = 0
        items_selected_by_greedy = []

        # Greedily selects the most valuable items until no more can be selected without exceeding the capacity
        for index, value, weight, _ in index_value_weight_ratio:
            if total_weight + weight <= capacity:
                items_selected_by_greedy.append(index)
                total_value += value
                total_weight += weight
            if time.time() - self.start_time > self.cut_off:  # Check if time limit has been exceeded
                print(f"Execution was cut off at {self.cut_off} seconds.")
                return

        # Define the minimum item value based on epsilon approximation parameter
        a = epsilon * total_value
        # Create a list of item indices where item value is less than or equal to 'a'
        Ia = [index for index, value, _, _ in index_value_weight_ratio if value <= a]

        max_subset_value = 0
        best_subset_indices = []

        # Set the maximum subset size based on the epsilon parameter
        max_subset_size = int(2 / epsilon)
        if Ia:
            # Generate all possible combinations of items within the subset size limit
            for subset_size in range(1, max_subset_size + 1):
                for subset_indices in combinations(Ia, subset_size):
                    if time.time() - self.start_time > self.cut_off:
                        print(f"Execution was cut off at {self.cut_off} seconds.")
                        self.total_value = max_subset_value
                        self.items_selected = sorted(best_subset_indices)
                        return

                    # Calculate the total weight and value of the current subset
                    subset_weight = sum(weights[index] for index in subset_indices)
                    subset_value = sum(values[index] for index in subset_indices)
                    current_subset_indices = list(subset_indices)

                    if subset_weight <= capacity:
                        remaining_capacity = capacity - subset_weight
                        # Sort remaining items by value-to-weight ratio in descending order
                        additional_items = [(index, values[index], weights[index]) for index in range(n) if index not in subset_indices]
                        additional_items.sort(key=lambda x: x[1] / x[2], reverse=True)

                        # Add more items if they fit in the remaining capacity
                        for index, value, weight in additional_items:
                            if weight <= remaining_capacity:
                                current_subset_indices.append(index)
                                subset_value += value
                                remaining_capacity -= weight

                        # Update the best subset found so far if the current value is higher
                        if subset_value > max_subset_value:
                            max_subset_value = subset_value
                            best_subset_indices = current_subset_indices

        self.total_value = int(max_subset_value)
        self.items_selected = sorted(best_subset_indices)
        print(f"Execution completed in {time.time() - self.start_time:.2f} seconds.")

    # Print and save the results
    def printResult(self):
        fileName = os.path.basename(self.filePath)
        print("Total value:", self.total_value)
        print("Items selected:", self.items_selected)

        # Create a directory for solutions if it does not exist
        sol_directory = "ApproxSolutions"
        if not os.path.exists(sol_directory):
            os.makedirs(sol_directory)

        # Save the solution to a file
        sol_file = f"{sol_directory}/{fileName}_Approx_{self.cut_off}.sol"
        with open(sol_file, "w") as file:
            file.write(f"{self.total_value}\n")
            file.write(",".join(map(str, self.items_selected)))

if __name__ == "__main__":
    pass
