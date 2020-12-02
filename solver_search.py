import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
from utils import convert_dictionary, calculate_stress_for_room
import sys
import random
import glob
from os.path import normpath, basename
import time

num_trials = 1000

stop_time = None


    


def try_partition_into_k_groups(k, G, s):
    threshold = s/k
    stressed_out = set()
    l = [i for i in range(20)]
    random.shuffle(l)
    maxi = -1
    ans = None
    cnt = 0
    timeout = False
    def dfs(cur, n):
        nonlocal timeout
        # if timeout:
        #     return
        # nonlocal cnt
        # if cnt % 10000 == 0:
        #     if time.time() > stop_time:
        #         timeout = True
        #         print('TIMEOUT')
        #         return
        # cnt += 1
        if n == 20:
            D = {}
            for i, group in enumerate(cur):
                for student in group:
                    D[student] = i
            # print(D)
            # assert is_valid_solution(D, G, s, k)
            happiness = calculate_happiness(D, G)
            nonlocal maxi
            nonlocal ans
            if happiness > maxi:
                maxi = happiness
                ans = D
                print(ans)
            return

        for i, group in enumerate(cur):
            if i > n:
                continue # 去重
            new_group = group + (l[n],)
            if new_group in stressed_out:
                continue
            # print(new_group)
            if calculate_stress_for_room(list(new_group), G) > threshold:
                stressed_out.add(new_group)
                continue
            dfs(cur[:i] + (new_group,) + cur[i+1:], n+1)
    dfs(tuple(() for _ in range(k)), 0)
    return ans




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
    # global stop_time
    # stop_time = time.time() + 60
    for k in [2]:
        D = try_partition_into_k_groups(k, G, s)
        if D is not None:
            return (D, k)
    return (None, None)




# Calculate the total stress in the room

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = solve(G, s)

#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'medium_try.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    cnt = 0
    inputs = glob.glob('inputs/medium_deleted/*')
    for input_path in inputs:
        cnt += 1
        right_now = basename(normpath(input_path))[:-3]
        output_path = 'outputs/medium_deleted/' + right_now + '.out'
        print(right_now, cnt)
        G, s = read_input_file(input_path)
        (D, k) = solve(G, s)
        if D is None:
            continue
        # assert is_valid_solution(D, G, s, k)
        # cost_t = calculate_happiness(D)
        write_output_file(D, output_path)
