import random
import time
import os

def random_solution(weights, values, capacity, num_items):
    solution = []
    total_weight = 0
    for i in range(num_items):
        if total_weight + weights[i] <= capacity:
            if random.random() > 0.5:
                solution.append(1)
                total_weight += weights[i]
            else:
                solution.append(0)
        else:
            solution.append(0)
    return solution

def calculate_value(solution, values):
    return sum(value * x for value, x in zip(values, solution))

def get_neighbor(solution, capacity, num_items, weights, values, min_change=1, max_change=None, change_percentage=0.1):
    neighbor = solution[:]

    # Determine max_change based on the percentage of num_items if not explicitly set
    if max_change is None:
        max_change = int(num_items * change_percentage)

    # Calculate the number of changes, ensuring it stays within specified bounds
    num_changes = random.randint(min_change, max_change)

    # Calculate value-to-weight ratio and create lists for additions and removals
    value_to_weight = [(values[i] / weights[i], i) for i in range(num_items)]
    add_candidates = sorted([item for item in value_to_weight if neighbor[item[1]] == 0], key=lambda x: x[0],
                            reverse=True)
    remove_candidates = sorted([item for item in value_to_weight if neighbor[item[1]] == 1], key=lambda x: x[0])

    # Attempt to remove items
    removed_count = 0
    for value_weight, index in remove_candidates:
        if removed_count >= num_changes:
            break
        neighbor[index] = 0
        removed_count += 1

    # Attempt to add items
    added_count = 0
    for value_weight, index in add_candidates:
        if added_count >= num_changes:
            break
        if sum(weights[i] for i, val in enumerate(neighbor) if val == 1) + weights[index] <= capacity:
            neighbor[index] = 1
            added_count += 1

    return neighbor

def hill_climbing(weights, values, capacity, num_items, cut_off_time, random_seed, file_path, method):
    random.seed(random_seed)
    start_time = time.time()
    best_solution = random_solution(weights, values, capacity, num_items)
    best_value = calculate_value(best_solution, values)
    trace = []
    trace.append((time.time() - start_time, best_value))

    no_improvement_streak = 0

    while time.time() - start_time < cut_off_time:
        if no_improvement_streak > 150:  # Arbitrary number; adjust as necessary
            best_solution = random_solution(weights, values, capacity, num_items)  # Random restart
            no_improvement_streak = 0

        neighbor = get_neighbor(best_solution, capacity, num_items, weights, values)
        neighbor_value = calculate_value(neighbor, values)
        if neighbor_value > best_value:
            best_solution = neighbor
            best_value = neighbor_value
            trace.append((time.time() - start_time, best_value))
            no_improvement_streak = 0
        else:
            no_improvement_streak += 1


    print(f"Running time is {time.time() - start_time}")
    save_results(file_path, method, cut_off_time, random_seed, best_solution, best_value)
    save_trace(file_path, method, cut_off_time, random_seed, trace)

def save_results(file_name, method, cutoff, seed, solution, value):
    solution_filename = f"{os.path.basename(file_name)}_{method}_{cutoff}_{seed}.sol"
    with open(solution_filename, 'w') as f:
        f.write(f"{int(value)}\n")
        indices = [str(index) for index, val in enumerate(solution) if val == 1]
        f.write(",".join(indices) + "\n")

def save_trace(file_name, method, cutoff, seed, trace):
    trace_filename = f"{os.path.basename(file_name)}_{method}_{cutoff}_{seed}.trace"
    with open(trace_filename, 'w') as f:
        for time_stamp, value in trace:
            f.write(f"{time_stamp:.2f},{int(value)}\n")

def run_LS2(filename, time_limit, seed, number_nodes, capacity, values, weights):
    hill_climbing(weights, values, capacity, number_nodes, time_limit, seed, filename, 'LS2')
