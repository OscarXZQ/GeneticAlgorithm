import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
from utils import convert_dictionary, calculate_stress_for_room, calculate_happiness_for_room
import sys
import random
import glob
from os.path import normpath, basename
import time

num_trials = 1000

stop_time = None

<<<<<<< HEAD
No1 = 2151.481
=======
top_score = {
    'medium-8': 2151.48,
    'medium-11': 265.269,
    'medium-14': 705.993,
    'medium-19': 425.417,
    'medium-20': 121.52,
    'medium-21': 2342.282,
    'medium-22': 1760.412
}


>>>>>>> c34d8b2ba5b5d4dc96e0dde72e97d2379ae8bfe7
    


def try_partition_into_k_groups(k, G, s, goal):
    threshold = s/k
    stressed_out = set()
    seen = dict()
    l = [i for i in range(20)]
    random.shuffle(l)
    found = False
    ans = None
    cnt = 0
    timeout = False
    maxi = -1

    def dfs(cur, n):
        nonlocal found
        if found or timeout:
            return
        # if timeout:
        #     return
        # nonlocal cnt
        # if cnt % 10000 == 0:
        #     if time.time() > stop_time:
        #         timeout = True
        #         print('TIMEOUT')
        #         returnmedium-8.in
        # cnt += 1
        if n == 20:
            happiness = 0
            for group in cur:
                if group in seen:
                    happiness += seen[group]
                else:
                    tmp = calculate_happiness_for_room(group, G)
                    seen[group] = tmp
                    happiness += tmp
            # print("Current happiness:",happiness)
            nonlocal ans
<<<<<<< HEAD

            if happiness > maxi:
                maxi = happiness
                D = {}
                for i, group in enumerate(cur):
                    for student in group:
                        D[student] = i
                ans = D
                print(ans, happiness)
            if happiness >= No1:
                return
=======
            nonlocal maxi
            if happiness > maxi:
                maxi = happiness
                print("Current happiness:",happiness)
                print(cur)
                if happiness >= goal:
                    print('FOUND!!!')
                    ans = cur
                    print(ans, happiness)
                    found = True
>>>>>>> c34d8b2ba5b5d4dc96e0dde72e97d2379ae8bfe7
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




def solve(G, s, goal):
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
<<<<<<< HEAD
    for k in range(6, 20):
        D = try_partition_into_k_groups(k, G, s)
        if D is not None:
=======
    for k in range(3,n+1):
        print("trying splitting into", k, "groups")
        ans = try_partition_into_k_groups(k, G, s, goal)
        if ans is not None:
            D = {}
            for i, group in enumerate(ans):
                for student in group:
                    D[student] = i
>>>>>>> c34d8b2ba5b5d4dc96e0dde72e97d2379ae8bfe7
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
<<<<<<< HEAD
    inputs = glob.glob('inputs/medium_deleted_three/medium-8.in')
=======
    inputs = glob.glob('inputs/medium_best_0/*.in')
>>>>>>> c34d8b2ba5b5d4dc96e0dde72e97d2379ae8bfe7
    for input_path in inputs:
        cnt += 1
        right_now = basename(normpath(input_path))[:-3]
        output_path = 'outputs/medium_deleted/' + right_now + '.out'
        print(right_now, cnt, top_score[right_now])
        G, s = read_input_file(input_path)
        (D, k) = solve(G, s, top_score[right_now])
        if D is None:
            continue
        # assert is_valid_solution(D, G, s, k)
        cost_t = calculate_happiness(D, G)
        print(cost_t)
        write_output_file(D, output_path)
