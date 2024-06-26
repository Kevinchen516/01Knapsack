"""
This code implement simulated annealing algorithm to the knapsack problem.
In addiction to normal parameters(values, weight, weight_threshold), this algorithm require iter_per_temp (iteration_time) for each temperature,
and it also needs initial_temp, final_temp for annealing control.
"""
import random
import math
import numpy as np
import time
import os


class LS1:
    def __init__(self, inst, n, weight_list, value_list, weight_threshold_value, random_seed, cut_off):

        # initial the 0-1 pack problem
        self.example_name = os.path.basename(inst)
        self.n = n
        self.weight_list = np.array(weight_list)
        self.value_list = np.array(value_list)
        self.weight_threshold_value = weight_threshold_value
        self.random_seed = random_seed
        self.initial_x = self.Initial_solution()
        self.local_best = self.evaluate(self.initial_x)
        self.cut_off = cut_off
        self.sol_file = " "
        self.trace_file = " "

    def input_size(self):
        if self.n < 50:
            self.sol_file = "LS1_ans\small\{}_LS1_{}_{}.sol".format(self.example_name, self.cut_off, self.random_seed)
            self.trace_file = "LS1_ans\small\{}_LS1_{}_{}.trace".format(self.example_name, self.cut_off,
                                                                        self.random_seed)
        else:
            self.sol_file = "LS1_ans\large\{}_LS1_{}_{}.sol".format(self.example_name, self.cut_off, self.random_seed)
            self.trace_file = "LS1_ans\large\{}_LS1_{}_{}.trace".format(self.example_name, self.cut_off,
                                                                        self.random_seed)

    def evaluate(self, x):
        """
        Caluculate the total value and total weight of one input array x.

        Inputs:
            np.array: x

        Returns:
            list: [totalValue,totalWeight]
        """
        picked = x
        totalValue = np.dot(picked, self.value_list)  # compute the value of the knapsack selection
        totalWeight = np.dot(picked, self.weight_list)  # compute the weight value of the knapsack selection
        return [totalValue, totalWeight]

    def flip_neighborhoods(self, x):
        """
        Random pick one neighbourhood.

        Input:
            np.array: x.
        Returns:
            np.array: x_new.
        """
        # change_idx_list = random.sample(range(self.n),round(self.n/2))
        if self.n < 5:
            change_idx_list = random.sample(range(self.n), 1)
        else:
            change_idx_list = random.sample(range(self.n), 3)
        new_x = np.copy(x)

        for idx in change_idx_list:
            if x[idx] == 1:
                new_x[idx] = 0
            else:
                new_x[idx] = 1

        return new_x

    def Initial_solution(self):
        """
        Initialize the solution using Greedy alg.

        Returns:
            np.array: x.
        """
        # Seeds
        np.random.seed(self.random_seed)
        random.seed(self.random_seed)
        unit_value = [(self.value_list[i] / self.weight_list[i], i) for i in range(self.n)]
        unit_value.sort(reverse=True)

        # Initial the array with greedy method
        x = np.zeros(self.n)
        total_weight = self.weight_threshold_value * 0.85

        for unit_value, idx in unit_value:
            if self.weight_list[idx] <= total_weight:
                x[idx] = 1
                total_weight -= self.weight_list[idx]
        return x

    # def Initial_solution(self):
    #     """
    #     Initialize the solution.

    #     Returns:
    #         np.array: x.
    #     """
    #     # Seeds
    #     np.random.seed(self.random_seed)
    #     random.seed(self.random_seed)
    #     init_idx_list = random.sample(range(self.n),10)

    #     # Initial the array with greedy method
    #     x = np.zeros(self.n)
    #     for idx in init_idx_list:
    #         x[idx] = 1
    #     while (self.evaluate(x)[1]>self.weight_threshold_value):
    #         init_idx_list = random.sample(range(self.n),10)
    #         x = np.zeros(self.n)
    #         for idx in init_idx_list:
    #             x[idx] = 1

    #     return x

    def simulated_Annealing(self, initial_temp, iter_per_temp, final_temp):
        """
        Run the annealing simulation.

        Inputs:
            int: initial_temp.
            int: iter_per_temp.
            int: final_temp.
        Returns:
            np.array: x.
        """
        # Seeds
        np.random.seed(self.random_seed)
        random.seed(self.random_seed)

        # Make direction
        try:
            os.mkdir("LS1_ans")
        except FileExistsError:
            pass

        # Make direction
        try:
            os.mkdir("LS1_ans/large")
            os.mkdir("LS1_ans/small")
        except FileExistsError:
            pass

        start_time = np.float64(time.time())

        self.input_size()

        with open(self.trace_file, "w") as file:

            x_curr = self.initial_x  # x_curr will hold the current solution
            x_best = x_curr[:]  # x_best will hold the best solution
            ans_best = self.evaluate(x_best)

            current_end = np.float64(time.time())
            # print(round(current_end-start_time,2),self.local_best[1],self.local_best[0]) #  # print the weight and value
            input_str = str(current_end - start_time) + " " + str(int(self.local_best[0]))
            file.write(input_str + "\n")

            while (initial_temp > final_temp):

                # Time restriction
                current_end = np.float64(time.time())
                if round(current_end - start_time, 2) > self.cut_off:
                    # write the current best
                    update_str = str(current_end - start_time) + " " + str(int(self.evaluate(x_best)[0]))
                    file.write(update_str + "\n")
                    return x_best

                m = 0  # Counting iteration in current temp
                k = 1  # The constant

                # Iteration in every temperature
                while (m <= iter_per_temp):
                    m += 1

                    # Generate neighbourhood
                    s = self.flip_neighborhoods(x_curr)
                    s_evaluate = self.evaluate(s)

                    # Can't be bigger than the threshold
                    if (s_evaluate[1] <= self.weight_threshold_value):
                        # get a better value
                        if (s_evaluate[0] > ans_best[0]):
                            x_best = s[:]
                            x_curr = s[:]
                            ans_best = s_evaluate[:]
                            # print(initial_temp," ",s_evaluate[:])
                            current_end = np.float64(time.time())
                            update_str = str(current_end - start_time) + " " + str(int(s_evaluate[0]))
                            # update_str = str(round(current_end-start_time,2)) + " " + str(int(s_evaluate[1]))
                            file.write(update_str + "\n")
                        # Probability
                        else:
                            delta = self.evaluate(x_curr)[0] - self.evaluate(s)[0]
                            change_or_not = random.uniform(0, 1)
                            randomness = math.exp(-1 * delta / k / (initial_temp))
                            if (change_or_not < randomness):
                                x_curr = s[:]

                initial_temp = initial_temp * 0.998  # Update the temperature

            # reach the final temperature
            # current_end = np.float64(time.time())
            # final_str = str(round(current_end-start_time,2)) + " " + str(int(ans_best[1]))
            # file.write(final_str + "\n")

            return x_best
        # return self.initial_x,x_best

    def save_solution(self, x):
        """
        Write the answer to the file.

        Inputs:
            np.array: x
        """
        best_value = str(self.evaluate(x)[0])
        with open(self.sol_file, "w") as file:
            file.write(best_value + '\n')
            indices = np.where(x == 1)[0]
            index_str = ','.join(map(str, indices))
            file.write(index_str)

