import random
import math
import numpy as np
import time
import os

class LS1:
    def __init__(self, n, weight_list, value_list, weight_threshold_value, random_seed, cut_off):

        # initial the 0-1 pack problem
        self.n = n
        self.weight_list = np.array(weight_list)
        self.value_list = np.array(value_list)
        self.weight_threshold_value = weight_threshold_value
        self.random_seed = random_seed
        self.initial_x = self.Initial_solution()
        self.local_best = self.evaluate(self.initial_x)
        self.cut_off = cut_off
    
    # def Initial_solution(self):
    #     # Seeds
    #     np.random.seed(self.random_seed)
    #     random.seed(self.random_seed)
    #     x = np.zeros(self.n)
    #     return x

    # def OneflipNeighborhood(self,x):
    #     nbrhood = []

    #     for i in range(0, self.n):
    #         temp=list(x)
    #         nbrhood.append(temp)
    #         if nbrhood[i][i] == 1:
    #             nbrhood[i][i] = 0
    #         else:
    #             nbrhood[i][i] = 1

    #     return nbrhood

    def evaluate(self,x):
        picked = x
        totalValue = np.dot(picked, self.value_list)  # compute the value of the knapsack selection
        totalWeight = np.dot(picked, self.weight_list)  # compute the weight value of the knapsack selection
        return [totalValue,totalWeight]
    
    def flip_neighborhoods(self,x):
        # change_idx_list = random.sample(range(self.n),round(self.n/2))
        change_idx_list = random.sample(range(self.n),1)
        new_x = np.copy(x)

        for idx in change_idx_list:
            if x[idx] == 1:
                new_x[idx] = 0
            else:
                new_x[idx] = 1

        return new_x

    def Initial_solution(self):
        # Seeds
        np.random.seed(self.random_seed)
        random.seed(self.random_seed)
        unit_value = [(self.value_list[i]/self.weight_list[i], i) for i in range(self.n)]
        unit_value.sort(reverse=True)

        # Initial the array with greedy method
        x = np.zeros(self.n)
        total_weight = self.weight_threshold_value*0.9

        for unit_value, idx in unit_value:
            if self.weight_list[idx] <= total_weight:
                x[idx] = 1
                total_weight -= self.weight_list[idx]
        return x

    def simulated_Annealing(self, initial_temp, iter_per_temp, final_temp):
        # Seeds
        np.random.seed(self.random_seed)
        random.seed(self.random_seed)

        start_time = np.float64(time.time())
        
        x_curr = self.initial_x  # x_curr will hold the current solution
        x_best = x_curr[:]  # x_best will hold the best solution
        ans_best = self.evaluate(x_best)

        current_end = np.float64(time.time())
        print(round(current_end-start_time,2),self.local_best[1],self.local_best[0]) #  # print the weight and value

        k=0
        
        while (initial_temp/(k+1) > final_temp):

            # Time restriction
            current_end = time.time()
            if round(current_end-start_time,2) > self.cut_off:
                return x_best

            m = 0 # Counting iteration in current temp

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
                        print(s_evaluate[:])
                    # Probabl
                    else:
                        delta = self.evaluate(x_curr)[0] - self.evaluate(s)[0]
                        change_or_not = random.uniform(0,1)
                        randomness= math.exp(-1 * delta * (k+1) / (initial_temp))
                        if (change_or_not < randomness):
                            x_curr=s[:]
            current_end = time.time()
            loop_evaluate = self.evaluate(x_curr)
            print(round(current_end-start_time,2),loop_evaluate[1],loop_evaluate[0]) # print [weight, value] for one temperature loop
                
            current_end = np.float64(time.time())
            k = k + 1
        return x_best
        # return self.initial_x,x_best

    def save_solution(self,x):
        best_value = str(self.evaluate(x)[0])
        file_name = "LS1_ans\example_LS1_{}_{}.trace".format(self.cut_off,self.random_seed)
        try:
            os.mkdir("LS1_ans")
        except FileExistsError:
            pass
        with open (file_name,"w") as file:
            file.write(best_value + '\n')
            for item in x:
                file.write(str(item)+" ")
    
