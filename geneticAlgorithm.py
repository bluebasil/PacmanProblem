from operator import attrgetter
import numpy as np
import sys
import random
import math
import copy
import pacman

"""
A genetic algorithm that attempts to find the optimal path to collect all of the coins
based off of the pacman problem's board
Board size, starting position, and walls are specified with an input file of the same
format as the pacman input file (path can be empty).

TODO:
    -Create a better stoping condition
    -try k-point crossovers
    -experiment with different variations on mutation
"""


siblings = 1000
# Currently the only stopping condition is this number of generations.  Better stopping conditions may be nice
num_generations = 500
# I ahev found that 1 works well here on my test boards
mutation_rate = 1
# This can be any number >= 1
# The lower it is, the shorter the intial paths will be, and the algorithm will mostly focus on getting all coins.  
# The larger it is, the larger initial path lengths, and the algorithm will mostly focus on finding faster routes
path_start_ratio = 1.5


# Open file and intialize board
if(len(sys.argv) != 2):
    print("Requires 1 input file")
    exit()

try:
    f = open(sys.argv[1])
except IOError:
    print("Error opening file")
    exit()

# File must include board size and starting position at least
lines = f.readlines()
if(len(lines) < 2):
    print("Not enought lines")
    exit()

# Close file
try:
    f.close()
except IOError:
    print("Error closing file")
    exit()

# Get board size
try:
    w, h = (int(s) for s in lines[0].split())
except ValueError:
    print("Non-int in input")
    exit()
motherboard = np.ones((w, h))

# Helper function for detecting errors in input file
def good_position(x, y):
    if (x < 0 or x >= motherboard.shape[0] or y < 0 or y >= motherboard.shape[1] or motherboard[x,y] > 1):
        return 0
    return 1

# Get wall positions
for line in lines[3:]:
    try:
        x, y = (int(s) for s in line.split()) 
    except ValueError:
        print("Non-int in input")
        exit()
    if(good_position(x, y)):
        motherboard[x,y] = 3
    else:
        print("wall outside of board or on top of another wall")
        exit()

# Get starting position
try:
    start_x, start_y = (int(s) for s in lines[1].split())
except ValueError:
    print("Non-int in input")
    exit()
if(good_position(start_x, start_y)):
    motherboard[start_x,start_y] = 0
else:
    print("Starting position outside of board or on top of wall")
    exit()




class path_set:
    path = ""
    score = -1
    fitness = -1
    def print_me(self):
        print(f"{self.score}  in {len(self.path)} moves")

# prints the batch of the current paths, used in debugging
def print_siblings(paths):
    for p in paths:
        p.print_me()

# Returnes the average fitness of all the paths.  Used in analytics
def average_fitness(paths):
    tot = 0
    for p in paths:
        tot += p.fitness
    return tot/len(paths)

# a very simple fitness function.  Tries to balance # of coins collected and path length
def calculate_fitness(path_obj):
    return path_obj.score**2 / len(path_obj.path)

# Runs the computational part of the pacman solution which returns
# the final x and y position, along with # of coins (x and y position ignored)
def run_inhouse(path_obj):
    fresh_board = copy.deepcopy(motherboard)
    x, y, score = pacman.compute(fresh_board,start_x,start_y,path_obj.path)
    path_obj.score = score
    path_obj.fitness = calculate_fitness(path_obj)


# preform a single point crossover from two parents
# k-point crossover may be better for this problem but uniform crossover is not 
# practical for this problem
def crossover(p1, p2):
    point = random.randint(1,min(len(p1.path),len(p2.path)))
    combined = p1.path[:point] + p2.path[point:]
    #print(min(len(p1.path),len(p2.path)), len(combined))
    return combined

# preforms point mutations based on mutation rate
# I chose to choose spots to mutate with replacement
def mutation(child_path):
    num_mutations = random.randint(0,int(len(child_path) * mutation_rate))
    for i in range(num_mutations):
        spot = random.randint(0,len(child_path)-1)
        child_path = child_path[:spot] + generate_cardinal() + child_path[spot+1:]
    return child_path

# Has a chance to drop a random part of the path
# This is the only method which shortens the path
def drop(child_path):
    start = random.randint(0,len(child_path)-1)
    # On small inputs, end-start is rarely positine.  Ceiling allows this to work much better
    end = math.ceil(np.random.normal(start, len(child_path)*0.05, 1))
    if(end-start > 0):
        child_path = child_path[:start] + child_path[end:]
    return child_path

# This was just an experiment of mine.  It does not help
def swap_crossover(child_path):
    if(random.random() < mutation_rate/4):
        point = random.randint(0,len(child_path)-1)
        child_path = child_path[point:] + child_path[:point]
    return child_path

def evolution(paths):
    global siblings
    generation = 0
    #for analytics
    f = open("export.csv","w")
    while(generation < num_generations):
        # Most fit path will be at the start of the list
        paths = sorted(paths,key=attrgetter('fitness'), reverse = True)

        print(f"\nGeneration {generation}:")
        print(f"Top score: {paths[0].score} in {len(paths[0].path)} moves (fitness: {paths[0].fitness})")
        f.write(f"{generation},{paths[0].score},{len(paths[0].path)},{paths[0].fitness},{average_fitness(paths)}\n")
        print(f"Optimal path: {paths[0].path}")
        generation += 1

        parents = int(siblings/5)
        for i in range(parents+1,siblings):
            #print('|', end='')
            child_path = crossover(random.choice(paths[:parents]),random.choice(paths[:parents]))
            child_path = mutation(child_path)
            child_path = drop(child_path)
            #child_path = swap_crossover(child_path)
            paths[i].path = child_path
            #test path and calculate fitness
            run_inhouse(paths[i])
    f.close()

def generate_cardinal():
    return random.choice("NSEW")

# generates initial paths
def generate_random_path():
    global w, h
    new_path = ""
    # initial paths will be of size w*h* the path start ratio.  with no walls, the optimal path should be equal to w*h-1
    for i in range(int(w*h*path_start_ratio)):
        new_path += generate_cardinal()
    return new_path

#initialize
paths = np.empty(siblings, dtype=object)
for i in range(siblings):
    new_path = path_set()
    new_path.path = generate_random_path()
    run_inhouse(new_path)
    paths[i] = new_path

evolution(paths)