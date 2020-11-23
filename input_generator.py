import networkx as nx
from parse import write_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, convert_dictionary, calculate_happiness_for_room, calculate_stress_for_room
import sys
import random

def generate(room_to_student):
    '''
    :param room_to_student: dictionary mapping from room to student
    :return: input file
    '''
    s_max = 99.5
    k = len(room_to_student)
    threshold = round (s_max / k , 3)
    G = nx.Graph()
    # create graph
    for room in room_to_student.keys():
        for student in room_to_student[room]:
            G.add_node(student, room = room)

    edgeList = [(u, v) for u in G.nodes() for v in G.nodes() if u < v]
    G.add_edges_from(edgeList, happiness = 0, stress = 0)

    # assign random stress and happiness levels
    for u, v in G.edges():
        if u < v:
            G[u][v]['stress'] = round(random.uniform(35, 100), 3)
            G[u][v]['happiness'] = round(random.uniform(50, 100), 3)
            

    # list of sums for each room
    stress_sums_for_rooms = [calculate_stress_for_room(room_to_student[room], G) for room in room_to_student.keys()]
    happiness_sums_for_rooms = [calculate_happiness_for_room(room_to_student[room], G) for room in room_to_student.keys()]
    min_happiness_for_rooms = [min_happiness_for_room(room_to_student, room, G) for room in room_to_student.keys()]
    # adjustment for stress and happiness
    for u in G.nodes():
        for v in G.nodes():
            if u < v:
                if G.nodes[u]['room'] == G.nodes[v]['room']:
                    stress_sum = stress_sums_for_rooms[G.nodes[u]['room']]
                    G[u][v]['stress'] = round(G[u][v]['stress'] / stress_sum * threshold - random.uniform(0,0.1), 3)
                    print(G[u][v]['stress'], G[u][v]['happiness'])
                else:
                    offset = round(random.uniform(0, 1), 3)
                    room1, room2 = G.nodes[u]['room'], G.nodes[v]['room']
                    minimum_happiness_between_rooms = min(min_happiness_for_rooms[room1], min_happiness_for_rooms[room1])
                    G[u][v]['stress'] = round(threshold + offset ,3)
                    G[u][v]['happiness'] = round(minimum_happiness_between_rooms - offset , 3)
                    print((G[u][v]['stress'], G[u][v]['happiness']))
                    
    n = len(G.nodes())
    write_input_file(G, s_max, str(n) + ".in")
    write_output_file(convert_dictionary(room_to_student), str(n) + ".out")
    return G

def stress_between_rooms(room_to_student, room1, room2, G):
    stress_between_sum = 0
    for u in room_to_student[room1]:
        for v in room_to_student[room2]:
            stress_between_sum += G[u][v]['stress']
    return stress_between_sum


def happiness_between_rooms(room_to_student, room1, room2, G):
    happiness_between_sum = 0
    for u in room_to_student[room1]:
        for v in room_to_student[room2]:
            happiness_between_sum += G[u][v]['happiness']
    return happiness_between_sum


def min_happiness_for_room(room_to_student, room, G):
    min_happiness = float('infinity')
    for u in G.nodes():
        for v in G.nodes():
            if u < v:
                if G.nodes[u]['room'] == room and G.nodes[u]['room'] == G.nodes[v]['room']:
                    min_happiness = min(G[u][v]['happiness'], min_happiness)
    return min_happiness
