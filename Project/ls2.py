import random
import time
import os

def random_solution(weights, capacity, num_items):
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

def get_neighbor(solution, capacity, num_items, weights):
    neighbor = solution[:]
    num_changes = random.randint(1, num_items // 2)
    indices = random.sample(range(num_items), num_changes)
    for index in indices:
        neighbor[index] = 1 - neighbor[index]
    if sum(weight * n for weight, n in zip(weights, neighbor)) > capacity:
        return solution
    return neighbor

def hill_climbing(weights, values, capacity, num_items, cut_off_time, random_seed, file_path, method):
    random.seed(random_seed)
    start_time = time.time()
    best_solution = random_solution(weights, capacity, num_items)
    best_value = calculate_value(best_solution, values)
    trace = []

    iterations = 0
    while time.time() - start_time < cut_off_time:
        iterations += 1
        neighbor = get_neighbor(best_solution, capacity, num_items, weights)
        neighbor_value = calculate_value(neighbor, values)
        if neighbor_value > best_value:
            best_solution = neighbor
            best_value = neighbor_value
            trace.append((time.time() - start_time, best_value))
            if iterations % 100 == 0:
                save_trace(file_path, method, cut_off_time, random_seed, trace)

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

