for i in {1..10}
do
    python3 starter.py -inst "./DATA/DATASET/small_scale/small_$i" -alg BnB -time 10 -seed 5
done
