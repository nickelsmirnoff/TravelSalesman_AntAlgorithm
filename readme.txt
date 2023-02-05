Use this proect for researching Ant algorithm for travelling salesman problem(TSP)

file 1:
TSP generator full enumeration.py
is a script for generating TSP matrix and solving with full enumeration.
It creates a folder "Result" in the same directory and fills it with some .txt files
containing a matrix, best route and optimal distance for TSP/
!Carefully change the parameter N, if it is more than 11, script will work very long time!

file 2:
AntSolver.py
is a script for solving TSP with an Ant algorithm
it takes all files from folder "Input", reads it and tries to solve them with Ant algorithm.
this script contains a class Ant for creating Ants in TSP
Function AntAlgorithmSolver has a lot of parameters:

D - distance matrix for TSP
alpha, beta, Q, ro - Ant algorithm parameters
AntNumber - number of created ants for solving TSP
IterNumber - number of iterations of the ant algorithm. Better use 10000 or more