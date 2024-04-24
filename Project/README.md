# To start the Program
`All 4 Algorithms require 4 parameters -inst -alg -time -seed, even if some algorithm do not need all of them`
## For BnB
```python
python3 starter.py -inst ./DATA/DATASET/large_scale/large_10 -alg BnB -time 1 -seed 5 
```
The program will write the result trace file in BnB_trace and solution file in BnB_sol.
## For LS1(Simulated Annealing)
```python
python3 starter.py -inst ./DATA/DATASET/large_scale/large_10 -alg LS1 -time 1 -seed 5 
```
You can modify this in ```starter.py```
```python 
simulated_Annealing(initial_temp = 100000, iter_per_temp = 1500, final_temp=5)
```
to test different parameters
## For LS2(Hill Climbing)
```python
python3 starter.py -inst ./DATA/DATASET/large_scale/large_10 -alg LS2 -time 100 -seed 5 
```
The output trace file will be automatically written to the local directory. The trace files and solution files that I get from the evaluation are in the `./trace_hillclimbing` directory.
## For Approximation Algorithm

using Python 3.9
```
python starter.py -inst ./DATA/DATASET/test/KP_s_01 -alg Approx -time 300 -seed 0
```
The Approximation algorithm will run and output *.sol in ./Project/ApproxSolutions
```
Parameters:
-inst the input trace file
-alg  the algorithm need to run, for Approx is Approx
-time the cutting off time(second)
-seed unused for approximation algorithm
```
