import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
from utils import convert_dictionary
import sys
import glob
import os
#import basename
#import normpath


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    # TODO: your code here!
    #pass
    nodes = list(G.nodes)
    result_dic = {}
    result_k = 0
    result_happiness = 0
    #lst = partition(nodes)
    lst = list(algorithm_u(nodes, 5))
    print(lst[0])
    print(len(lst))
    for part in lst:
        k = len(part)
        #if k != 5:
        #    continue
        d = {}
        for i in range(0, k):
            d[i] = part[i]
        d = convert_dictionary(d)
        if not is_valid_solution(d, G, s, k):
            continue
        happiness = calculate_happiness(d, G)
        if happiness > result_happiness:
            print(happiness)
            result_dic = d
            result_k = k
            result_happiness = happiness
    return result_dic, result_k        

def algorithm_u(ns, m):
    def visit(n, a):
        ps = [[] for i in range(m)]
        for j in range(n):
            ps[a[j + 1]].append(ns[j])
        return ps

    def f(mu, nu, sigma, n, a):
        if mu == 2:
            yield visit(n, a)
        else:
            for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v
        if nu == mu + 1:
            a[mu] = mu - 1
            yield visit(n, a)
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                yield visit(n, a)
        elif nu > mu + 1:
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = mu - 1
            else:
                a[mu] = mu - 1
            if (a[nu] + sigma) % 2 == 1:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v

    def b(mu, nu, sigma, n, a):
        if nu == mu + 1:
            while a[nu] < mu - 1:
                yield visit(n, a)
                a[nu] = a[nu] + 1
            yield visit(n, a)
            a[mu] = 0
        elif nu > mu + 1:
            if (a[nu] + sigma) % 2 == 1:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] < mu - 1:
                a[nu] = a[nu] + 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = 0
            else:
                a[mu] = 0
        if mu == 2:
            yield visit(n, a)
        else:
            for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v

    n = len(ns)
    a = [0] * (n + 1)
    for j in range(1, m + 1):
        a[n - m + j] = j - 1
    return f(m, n, 0, n, a)


# Calculate the overall possibilities of partitions
def partition(lst):
    result = []
    if len(lst) == 1:
        return [[lst]]
    first = lst[0]
    for remain in partition(lst[1:]):
        result += [[[first]] + remain]
        for i, subset in enumerate(remain):
            result += [remain[:i] + [[first] + subset] + remain[i+1:]]
    return result

# Only for testing purposes
def test():
    sth = list(range(1, 6))
    for lst in partition(sth):
        print(lst)

# Calculate the total happiness in the room
'''
def calculate_happiness(G, lst):
    result = 0
    for i in range(0, len(lst)):
        for j in range(i+1, len(lst)):
            a = lst[i]
            b = lst[j]
            happiness = G.edges[a][b]["happiness"]
            result += happiness
    return result
'''

# Calculate the total stress in the room

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    #assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, './test.out')

'''
# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('./inputs/small/*')
    for input_path in inputs:
        output_path = './outputs/' + os.path.basename(os.path.normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path, 100)
        D, k = solve(G, s)
        assert is_valid_solution(D, G, s, k)
        with open(output_path, 'w') as fo:
            goal = calculate_happiness(D, G)
            fo.write('Total Happiness: ' + str(goal) + '\n')
            for key, value in D.items():
                fo.write(str(key) + " " + str(value) + "\n")
            fo.close()
        #write_output_file(D, output_path)
'''
'''
if __name__ == '__main__':
    outputs = glob.glob('./outputs/small_naive/*')
    for output_path in outputs:
        with open(output_path, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(output_path, 'w') as fout:
            fout.writelines(data[1:])
'''