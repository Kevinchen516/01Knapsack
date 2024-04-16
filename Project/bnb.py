import time
import heapq
trace =""
time_ = 0
class Item:
    def __init__(self, weight, value, original_index):
        self.weight = weight
        self.value = value
        self.original_index = original_index

    def __repr__(self):
        return f"Item(original_index={self.original_index}, weight={self.weight}, value={self.value})"

class Node:
    def __init__(self, next_index, sum_time, sum_value, upperbound, path):
        self.next_index = next_index
        self.sum_time = sum_time
        self.sum_value = sum_value
        self.upperbound = upperbound
        self.path = path.copy()  # Ensure we copy the path to not modify the original

def calculate_upper_bound(index, current_time, current_value, items, capacity, number_nodes):
    result = current_value
    remaining_time = capacity - current_time
    while index < number_nodes and items[index].weight <= remaining_time:
        remaining_time -= items[index].weight
        current_value += items[index].value
        index += 1

    if index < number_nodes:
        result = current_value + remaining_time * (items[index].value / items[index].weight)

    return result

def solve(items, capacity, number_nodes,start_time):
    global trace
    pq = []
    initial_path = [0] * number_nodes
    initial_ub = calculate_upper_bound(0, 0, 0, items, capacity, number_nodes)
    initial_node = Node(0, 0, 0, initial_ub, initial_path)
    heapq.heappush(pq, (-initial_node.upperbound, initial_node))  # Use negative for max-heap
    best_value = 0
    best_path = [0] * number_nodes  # Ensure best_path is the size of number_nodes
    best =0
    while pq:
        _, current = heapq.heappop(pq)
        if current.upperbound <= best_value:
            continue
        elapsed_time = time.time() - start_time
        if (elapsed_time > time_):
            return best_value, best_path
        if(current.sum_value > best):
            trace = trace + str(elapsed_time) + " " + str(current.sum_value)+"\n"
            best =current.sum_value
        if current.next_index == number_nodes:
            if best_value < current.sum_value:
                best_path = current.path[:]  # Clone the path when it's a potential best
            best_value = max(best_value, current.sum_value)
        else:
            item = items[current.next_index]
            if current.sum_time + item.weight <= capacity:
                # Include current item
                new_path = current.path[:]
                new_path[item.original_index] = 1  # Set using original index
                new_time = current.sum_time + item.weight
                new_value = current.sum_value + item.value
                new_ub = calculate_upper_bound(current.next_index + 1, new_time, new_value, items, capacity, number_nodes)
                new_node = Node(current.next_index + 1, new_time, new_value, new_ub, new_path)
                heapq.heappush(pq, (-new_node.upperbound, new_node))
            # Exclude current item
            new_path = current.path[:]
            new_path[item.original_index] = 0  # Set using original index
            new_ub = calculate_upper_bound(current.next_index + 1, current.sum_time, current.sum_value, items, capacity, number_nodes)
            new_node = Node(current.next_index + 1, current.sum_time, current.sum_value, new_ub, new_path)
            heapq.heappush(pq, (-new_node.upperbound, new_node))

    return best_value, best_path



def run_BnB(filename, time_limit, seed, number_nodes, capacity, values, weights):
    global time_
    print(f"Running Branch and Bound Algorithm with file {filename}, time {time_limit}, seed {seed}")
    start_time = time.time()
    items = []
    time_ = time_limit
    for i in range(number_nodes):
        items.append(Item(weights[i],values[i],i))
    items.sort(key=lambda item: -item.value / item.weight)
    best_value, best_path = solve(items, capacity, number_nodes,start_time)
    print(f"Best Value: {best_value}")
    backtrace = [1 if x else 0 for x in best_path]
    print("Backtrace:", backtrace)
    print("Trace:\n",trace)
    # while True:
    #     time.sleep(0.1)  # simulating work
    #     elapsed_time = time.time() - start_time
    #     if elapsed_time > time_limit:
    #         print("Time limit exceeded. Stopping the algorithm.")
    #         return "Algorithm stopped due to time limit."
