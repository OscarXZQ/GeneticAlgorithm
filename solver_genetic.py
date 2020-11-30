import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room, convert_dictionary
import sys
import glob
from os.path import normpath, basename
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--popSize', action='store', dest='popSize', default=15, help='Population Size.', type=int)
parser.add_argument('--eliteSize', action='store', dest='eliteSize', default=2, help='Size of elites. The top ELITESIZE among living beings who will not mutate nor die.', type=int)
parser.add_argument('--mutationRate', action='store', dest='mutationRate', default=0.02, help='Mutation Rate.', type=float)
parser.add_argument('--generations', action='store', dest='generations', default=200, help='Number of generations to run this algorithm.', type=int)
parser.add_argument('--converge', action='store_true', dest='converge', default=False, help='If true, end algorithm when the score does not improve for PATIENCE generations.')
parser.add_argument('--patience', action='store', dest='patience', default=25, help='End algorithm when the score does not improve for PATIENCE generations.', type=int)
    

results = parser.parse_args()

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

class Fitness: #need to add the output for our result
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0
        self.result = {}
    
    def routeDistance(self): #calculate the stress level and happiness here
        for k in range(1, len(self.route)):
            D = {} #student to room
            group_list = [ [] for _ in range(k)]
            for i in range(k):
                D[self.route[i]] = i
                group_list[i].append(self.route[i])
            for i in range(k, len(self.route)):
                cur = self.route[i]
                # print(type(cur_node), cur_node)
                mini = float('inf')
                maxi = -float('inf')
                cur_group = None
                stress_group = None
                stress_out = False
                for group_num, group in enumerate(group_list):
                    happiness = sum(G[cur][other_person]['happiness'] for other_person in group if G.has_edge(cur, other_person))
                    group_copy = list(group)
                    group_copy.append(cur)
                    stress = calculate_stress_for_room(group_copy, G)
                    if stress < mini:
                        mini = stress
                        stress_group = group_num
                    if stress > s/k:
                        continue
                    if happiness > maxi:
                        cur_group = group_num
                        maxi = happiness # we can add tiebreaking here
                if cur_group == None:
                    cur_group = stress_group
                    stress_out = True
                D[cur] = cur_group
                group_list[cur_group].append(cur)
            if is_valid_solution(D, G, s, k):
                cur_val = calculate_happiness(D, G)
                self.result = D
                return cur_val
        return -1
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = float(self.routeDistance())
        return self.fitness

def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route

def initialPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population

def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

def mutatePopulation(population, mutationRate):
    mutatedPop = [population[0]]
    
    for ind in range(1, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

def geneticAlgorithmGenerations(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    print("Initial happiness: " + str(rankRoutes(pop)[0][1]))
    happiness = -float('inf')
    best = {}
    for i in range(0, generations):
        print(i)
        elite = rankRoutes(pop)[0]
        ans = Fitness(pop[elite[0]])
        if happiness < ans.routeFitness():
            best = ans.result
            happiness = elite[1]
        print("best so far:" + str(happiness))
        print(elite[1])
        print(ans.result)
        pop = nextGeneration(pop, eliteSize, mutationRate)
    
    print("Final happiness: " + str(happiness))
    print(best)
    return best

def geneticAlgorithmConvergence(population, popSize, eliteSize, mutationRate, patience):
    pop = initialPopulation(popSize, population)
    print("Initial happiness: " + str(rankRoutes(pop)[0][1]))
    happiness = -float('inf')
    best = {}
    streak = 0
    while streak <= patience:
        elite = rankRoutes(pop)[0]
        ans = Fitness(pop[elite[0]])
        if happiness < ans.routeFitness():
            best = ans.result
            happiness = elite[1]
            streak = 1
        else:
            streak += 1
        print("best so far:" + str(happiness))
        print(elite[1])
        print(ans.result)
        pop = nextGeneration(pop, eliteSize, mutationRate)
    
    print("Final happiness: " + str(happiness))
    print(best)
    return best


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    lst = list(G.nodes)
    cityList = lst
    random.shuffle(lst)
    if results.converge:
        return geneticAlgorithmConvergence(population=cityList, popSize=results.popSize, eliteSize=results.eliteSize, mutationRate=results.mutationRate, patience=results.patience) #adjust hyper parameter
    else:
        return geneticAlgorithmGenerations(population=cityList, popSize=results.popSize, eliteSize=results.eliteSize, mutationRate=results.mutationRate, generations=results.generations) #adjust hyper parameter


# Here's an example of how to run your solver.



# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     # assert len(sys.argv) == 2
#     # path = sys.argv[1]
#     path = 'inputs/large/large-1.in'
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'outputs/large/large-1-mut005.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
compare = []
if __name__ == '__main__':
    inputs = glob.glob('inputs/medium/*')
    for input_path in inputs:
        print(input_path)
        cur_file = basename(normpath(input_path))[:-3]
        output_path = 'outputs/medium_genetic_nov29/' + cur_file + '.out'
        G, s = read_input_file(input_path)
        D = solve(G, s)
        # D, k = solve(G, s)
        # assert is_valid_solution(D, G, s, k)
        final_happiness = calculate_happiness(D, G)
        print("Final Happiness:", final_happiness)
        write_output_file(D, output_path)
        compare.append(str(cur_file) + str(final_happiness))
    write_output_file(compare, "outputs/medium_genetic_nov29_log.txt")

