import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
from utils import convert_dictionary
import sys
import random

num_trials = 500

def try_partition_into_k_groups(k, G, s):
    '''
    Try partitioning the 
    '''
    if k == 1:
        D = {}
        for i in range(len(G)):
            D[i] = 0
        if is_valid_solution(D, G, s, k):
            return D
        else:
            return None

    maxi = -1
    ret = None
    for _ in range(num_trials):
        # Greedy MAX-K-CUT, could enhance by using better MAX-K-CUT algorithms
        seq = list(G.nodes())
        random.shuffle(seq)
        D = {} # student to room
        group_list = [ [] for _ in range(k)] # room to student
        
        for i in range(k):
            D[seq[i]] = i
            group_list[i].append(seq[i])

        for i in range(k, len(seq)):
            cur_node = seq[i]
            # print(type(cur_node), cur_node)
            mini = float('inf')
            cur_group = None
            for group_num, group in enumerate(group_list):
                stress = sum(G[i][other_person]['stress'] for other_person in group if G.has_edge(i, other_person))
                if stress < mini:
                    mini = stress
                    cur_group = group_num
            assert cur_group != None
            D[cur_node] = cur_group
            group_list[cur_group].append(cur_node)
        if (is_valid_solution(D, G, s, k)):
            cur_val = calculate_happiness(D, G)
            if cur_val > maxi:
                maxi = cur_val
                ret = D
    return ret



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
    # n = G.size()
    n = len(G)
    for k in range(1, n+1):
        D = try_partition_into_k_groups(k, G, s)
        if D is not None:
            return D, k
    assert False




# Calculate the total stress in the room

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
