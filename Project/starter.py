# main.py
import argparse
import bnb
import approx
import ls1
import ls2

def main():
    parser = argparse.ArgumentParser(description="Run specific algorithms with given parameters.")
    parser.add_argument("-inst", type=str, required=True, help="Input file name")
    parser.add_argument("-alg", type=str, choices=['BnB', 'Approx', 'LS1', 'LS2'], required=True, help="Algorithm to run")
    parser.add_argument("-time", type=int, required=True, help="Cutoff time in seconds")
    parser.add_argument("-seed", type=int, required=True, help="Random seed")
    args = parser.parse_args()

    # Load data
    n, capacity, values, weights = load_data(args.inst)

    if args.alg == 'BnB':
        bnb.run_BnB(args.inst, args.time, args.seed, n, capacity, values, weights)
    elif args.alg == 'Approx':
        pass
        #approx.run_Approx(args.inst, args.time, args.seed)
    elif args.alg == 'LS1':
        solution = ls1.LS1(args.inst, n,weights,values,capacity,args.seed,args.time)
        x_best = solution.simulated_Annealing(initial_temp = 10000, iter_per_temp = 1000, final_temp=5)
        solution.save_solution(x_best)
        #ls1.run_LS1(args.inst, args.time, args.seed)
    elif args.alg == 'LS2':
        #pass
        ls2.run_LS2(args.inst, args.time, args.seed, n, capacity, values, weights)

def load_data(inst):
    values = []
    weights = []
    with open(inst, 'r') as file:
        n, capacity = map(int, file.readline().strip().split())
        for _ in range(n):
            value, weight = map(int, file.readline().strip().split())
            values.append(value)
            weights.append(weight)
    return n,capacity,values, weights

if __name__ == "__main__":
    main()
