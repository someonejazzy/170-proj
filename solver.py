import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
from collections import Counter
import os
import math
import multiprocessing as mp

import numpy as np
import random
import heapq
from itertools import islice


def greedy_edges(OGgraph, num_k, num_c):
    H = OGgraph.copy()
    nodes_from_edges = [0] * (len(G))
    remove_edge_list = []
    shortest_path = nx.algorithms.shortest_paths.weighted.dijkstra_path(OGgraph, 0, len(G) - 1)
    path_length = nx.dijkstra_path_length(OGgraph, 0, len(G) - 1)
    dists = []
    for i in range(len(shortest_path) - 1):
        dists.append(
            (
                H[shortest_path[i]][shortest_path[i + 1]]["weight"],
                shortest_path[i],
                shortest_path[i + 1],
            )
        )
    dists.sort()
    k_count = 0
    c_count = 0
    heuristic = 1

    T = 1000
    while num_k > 0:
        if i >= len(dists):
            break
        if num_k - 1 < k_count:
            break
        curr_path_len_best = path_length
        B = H.copy()
        best_edge = (0, 0)
        best_path = shortest_path
        for i in range(0, len(dists)):
            J = H.copy()
            J.remove_edge(dists[i][1], dists[i][2])
            if nx.is_connected(J) == False:
                # print("HELLO")
                continue
            if nx.algorithms.shortest_paths.generic.has_path(J, 0, len(G) - 1):
                path_length_new = nx.dijkstra_path_length(J, 0, len(G) - 1)
                # prob = math.exp((curr_path_len_best - path_length_new) / (-T))
                if path_length_new > curr_path_len_best:
                    B = J.copy()
                    best_edge = (dists[i][1], dists[i][2])
                    curr_path_len_best = path_length_new
                    best_path = nx.algorithms.shortest_paths.weighted.dijkstra_path(
                        J, 0, len(G) - 1
                    )
                # elif random.random() < prob:
                #     T *= 0.98
                #     B = J.copy()
                #     best_edge = (dists[i][1], dists[i][2])
                #     curr_path_len_best = path_length_new
                #     best_path = nx.algorithms.shortest_paths.weighted.dijkstra_path(
                #         J, 0, len(G) - 1
                #     )

        H = B.copy()
        if best_edge == (0, 0):
            # print("HELLO IM BACK")
            break
        # print(nx.is_connected(H))
        remove_edge_list.append(best_edge)
        # print(best_edge[1])
        # print(best_edge[0])
        nodes_from_edges[best_edge[0]] = 1 / heuristic
        nodes_from_edges[best_edge[1]] = 1 / heuristic
        path_length = curr_path_len_best
        k_count += 1
        heuristic += 1
        dists = []
        for i in range(len(best_path) - 1):
            dists.append(
                (H[best_path[i]][best_path[i + 1]]["weight"], best_path[i], best_path[i + 1])
            )
        dists.sort()
    return nodes_from_edges, path_length, remove_edge_list


def greedy_best_edge_removal_small_medium(OGgraph, num_k, num_c):
    # GREEDILY SELECT BEST EDGE REMOVAL IN SHORTEST PATH for small and medium
    H = G.copy()
    remove_edge_list = []
    remove_city_list = []
    shortest_path = nx.algorithms.shortest_paths.weighted.dijkstra_path(G, 0, len(G) - 1)
    path_length = nx.dijkstra_path_length(G, 0, len(G) - 1)

    dists = []
    for i in range(len(shortest_path) - 1):
        dists.append(
            (
                H[shortest_path[i]][shortest_path[i + 1]]["weight"],
                shortest_path[i],
                shortest_path[i + 1],
            )
        )
    dists.sort()
    k_count = 0
    c_count = 0
    best_path_city = shortest_path
    best_path_road = shortest_path
    best_path = shortest_path
    while num_k > 0 and num_c > 0:
        if i >= len(dists):
            break
        if num_k - 1 < k_count:
            break
        if num_c - 1 < c_count:
            break
        curr_path_len_best_road = path_length
        curr_path_len_best_city = path_length
        B = H.copy()
        C = H.copy()
        best_edge = (0, 0)
        best_city = -1
        # print(best_path)
        # best path greedy
        for i in range(0, len(dists)):
            J = H.copy()
            J.remove_edge(dists[i][1], dists[i][2])
            if nx.is_connected(J) == False:
                continue
            if nx.algorithms.shortest_paths.generic.has_path(J, 0, len(G) - 1):
                path_length_new = nx.dijkstra_path_length(J, 0, len(G) - 1)
                if path_length_new > curr_path_len_best_road:
                    B = J.copy()
                    best_edge = (dists[i][1], dists[i][2])
                    curr_path_len_best_road = path_length_new
                    best_path_road = nx.algorithms.shortest_paths.weighted.dijkstra_path(
                        J, 0, len(G) - 1
                    )

        # best city greedy
        # print(best_path)
        for j in best_path:
            if j == 0 or j == (len(G) - 1):
                continue
            D = H.copy()
            D.remove_node(j)
            if nx.is_connected(D) == False:
                continue
            if nx.algorithms.shortest_paths.generic.has_path(D, 0, len(G) - 1):
                path_length_new = nx.dijkstra_path_length(D, 0, len(G) - 1)
                if path_length_new > curr_path_len_best_city:
                    C = D.copy()
                    best_city = j
                    curr_path_len_best_city = path_length_new
                    best_path_city = nx.algorithms.shortest_paths.weighted.dijkstra_path(
                        D, 0, len(G) - 1
                    )
                    # print(best_path_city)

        if best_edge == (0, 0):
            break
        if best_city == -1:
            break

        if curr_path_len_best_city< curr_path_len_best_road:
            H = B.copy()
            remove_edge_list.append(best_edge)
            path_length = curr_path_len_best_road

            best_path = best_path_road[:]
            k_count += 1
            # print("Deleted: ", best_edge)

        else:
            H = C.copy()
            # H.remove_node(best_city)
            remove_city_list.append(best_city)
            path_length = curr_path_len_best_city
            # print("here" , best_path_city)
            best_path = best_path_city[:]
            c_count += 1
            # print("Deleted: ", best_city)
        dists = []
        for i in range(len(best_path) - 1):
            dists.append(
                (H[best_path[i]][best_path[i + 1]]["weight"], best_path[i], best_path[i + 1])
            )
        dists.sort()
        # print(best_path)
        if nx.is_connected(H) == False:
            print("oh no")
            break
    return remove_city_list,remove_edge_list


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    # pass
    # A = nx.adjacency_matrix(G).todense()

    # return parameters
    remove_edge_list = []
    remove_city_list = []
    H = G.copy()

    # set k and c accordingly
    if len(G) <= 30:
        num_k = 15
        num_c = 1
    elif len(G) <= 50:
        num_k = 50
        num_c = 3
    else:
        num_k = 100
        num_c = 5

    #return create_heuristic(G, num_k, num_c, 0, 0, 0)
    return [], [], 1

def solve2(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    # pass
    # A = nx.adjacency_matrix(G).todense()

    # return parameters
    remove_edge_list = []
    remove_city_list = []
    H = G.copy()

    # set k and c accordingly
    if len(G) <= 30:
        num_k = 15
        num_c = 1
        #remove_city_list1, remove_edge_list1, her1 = create_heuristic(H,num_k, num_c, 9, 100, 13) # SMALL BEST i think
        #remove_city_list2, remove_edge_list2, her2 = create_heuristic(H,num_k, num_c, 10, 40, 3) # MEDIUM BEST i think
        #remove_city_list3, remove_edge_list3, her3 = create_heuristic(H,num_k, num_c, 3, 80, 27) #random
        #remove_city_list4, remove_edge_list4, her4 = create_heuristic(H,num_k, num_c, 6, 100, 23) #random
        #remove_city_list5, remove_edge_list5, her5 = create_heuristic(H,num_k, num_c, 11, 105, 11) # SMALL BEST i think
    elif len(G) <= 50:
        num_k = 50
        num_c = 3
    else:
        num_k = 100
        num_c = 5
    remove_city_list1, remove_edge_list1, her1 = create_heuristic(H,num_k, num_c, 9, 100, 13) # SMALL BEST i think
    remove_city_list2, remove_edge_list2, her2 = create_heuristic(H,num_k, num_c, 10, 40, 3) # MEDIUM BEST i think
    remove_city_list3, remove_edge_list3, her3 = create_heuristic(H,num_k, num_c, 3, 80, 27) #random
    remove_city_list4, remove_edge_list4, her4 = create_heuristic(H,num_k, num_c, 5, 110, 20) #random
    #best_val = max(her1,her2)
    #her3, her4 = 0, 0
    #her2, her4 = 0, 0
    best_val = max(her1,her2,her3,her4)
    if(best_val == her1):
        print("1")
        return remove_city_list1, remove_edge_list1, 1
    if(best_val == her2):
        print("2")
        return remove_city_list2, remove_edge_list2, 2
    if(best_val == her3):
        print("3")
        return remove_city_list3, remove_edge_list3, 3
    if(best_val == her4):
        print("4")
        return remove_city_list4, remove_edge_list4, 4
    # big bad graph(s) time aaaa
    # notes: find node that repeats the most time, remove that node, run the whole thing again

def k_shortest_paths(G, source, target, k, weight=None):
  return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))


def create_heuristic(Ograph, num_edge, num_city, bat, her_c, dec_num):
	edges_removed = 0
	cities_removed = 0
	remove_edge_list = []
	remove_city_list = []

	batch = bat
	used_node = False
	while(edges_removed<num_edge or cities_removed<num_city):
		paths = k_shortest_paths(Ograph, 0, len(G)-1, batch, weight='weight')
		edge_her = {}
		city_her = {}
		her_cnt = her_c
		#her_cnt = 1
		path_cnt = 0
		for path in paths:
			path_cnt+=1
			for i in range(len(path)-1):
				if(path_cnt == 1):
					city_her[path[i]] = city_her.get(path[i], 50) + her_cnt
					edge_her[(path[i], path[i+1])] = edge_her.get((path[i], path[i+1]), 50) + her_cnt
					#her_cnt -= 13
					continue
				if(path[i] in city_her):
					city_her[path[i]] = city_her.get(path[i]) + her_cnt
				if((path[i], path[i+1]) in edge_her):
					edge_her[(path[i], path[i+1])] = edge_her.get((path[i], path[i+1])) + her_cnt #1/her_cnt
			her_cnt -= dec_num
			#her_cnt +=1
		edge_her = dict(sorted(edge_her.items(), key=lambda item: item[1], reverse = True))
		city_her = dict(sorted(city_her.items(), key=lambda item: item[1], reverse = True))

		J = Ograph.copy()
		H = Ograph.copy()
		edge_iter = iter(edge_her)
		city_iter = iter(city_her)
		best_edge = None
		best_node = None

		i = 0
		while(i < 1):
			if(edges_removed >= num_edge):
				break
			C = J.copy()
			remove_edge = next(edge_iter, None)
			if(remove_edge == None):
				break
			if(not C.has_node(remove_edge[1]) or not C.has_node(remove_edge[0])):
				continue
			if(not C.has_edge(remove_edge[0], remove_edge[1])):
				continue
			C.remove_edge(remove_edge[0], remove_edge[1])
			if(nx.is_connected(C)):
				best_edge = remove_edge
				J = C.copy()
				i+=1
			else:
				continue
		edge_graph = J.copy()
		
		i = 0
		while(i < 1):
			if(cities_removed >= num_city):
				break
			C = H.copy()
			remove_city = next(city_iter, None)
			if(remove_city == None):
				break
			if(not C.has_node(remove_city)):
				continue
			if(remove_city == 0 or remove_city == len(G)-1):
				continue
			C.remove_node(remove_city)
			if(nx.is_connected(C)):
				best_node = remove_city
				H = C.copy()
				i+=1
			else:
				continue
		if(best_node != None):
			node_graph = H.copy()
			#node_cost = nx.dijkstra_path_length(node_graph, 0, len(G)-1)
			#edge_cost = nx.dijkstra_path_length(edge_graph, 0, len(G)-1)
			#try comparing heuristics instead of costs
			if(best_edge == None or city_her[best_node]>edge_her[best_edge]):
				#print(node_cost, " ", edge_cost)
				remove_city_list.append(best_node)
				cities_removed +=1
				temp = remove_edge_list.copy()
				for edge in temp:
					if(edge[0] == best_node or edge[1] == best_node):
						remove_edge_list.remove(edge)
						edges_removed-=1
				Ograph = node_graph.copy()
			else:
				if(best_edge != None):
					remove_edge_list.append(best_edge)
					edges_removed +=1
					Ograph = edge_graph.copy()
		elif(best_edge != None):
			remove_edge_list.append(best_edge)
			edges_removed +=1
			Ograph = edge_graph.copy()
		else:
			break
	val = nx.dijkstra_path_length(Ograph, 0, len(G)-1)
	return remove_city_list, remove_edge_list, val

def min_cut_life(G, num_k, num_c):
    # SARTHAK MIN CUTS LIFE
    # print(G.edges().data())
    # set capacity to be 1/weight so that min cut priortizes includes shortest edges
    # print(G.nodes())
    ST_pairs = [[[(0, len(G) - 1)]]]
    Graph_List = [[H]]

    for edge in G.edges().data():
        H[edge[0]][edge[1]]["capacity"] = 1.0 / edge[2]["weight"]

    partition_cnt = 0
    while num_k > 0 and num_c > 0:
        if partition_cnt >= 100:
            break
        # get the set of edges in the min cut
        # compare all partitions of the graph and only do the max min cut of all partitions(can be optimized by storing paritions in a list/priority queue)
        max_cut_val = -1
        # print(partition_cnt)
        cutset = None
        for i in range(0, len(ST_pairs[partition_cnt])):
            # print(s_list)
            # print(t_list)
            # print(str(s_list[partition_cnt][i]) + " " + str(t_list[partition_cnt][i]))
            # print(ST_pairs[partition_cnt][i][0][0])
            if ST_pairs[partition_cnt][i][0][0] == ST_pairs[partition_cnt][i][0][1]:
                continue
            cut_val, partition = nx.minimum_cut(
                H, ST_pairs[partition_cnt][i][0][0], ST_pairs[partition_cnt][i][0][1]
            )
            reachable, non_reachable = partition
            if cut_val > max_cut_val:
                cutset = set()
                for u, nbrs in ((n, H[n]) for n in reachable):
                    cutset.update((u, v, H[u][v]["capacity"]) for v in nbrs if v in non_reachable)
                cutset = list(cutset)
                cutset.sort(reverse=True, key=lambda x: x[2])
                max_cut_val = cut_val

        # print("cutset is: " , cutset)
        # remove all edges(disconnects graph)
        # we don't check which nodes are disconnected yet. Can be done by checking adjacency list?
        if cutset == None:
            break
        for i in range(0, len(cutset) - 1):
            H.remove_edge(cutset[i][0], cutset[i][1])
            remove_edge_list.append((cutset[i][0], cutset[i][1]))
            num_k -= 1
            if num_k == 0:
                break
            # Check if a node is disconnected and add to list
            # could be more efficent
            for node, val in H.degree():
                if val == 0:
                    num_c -= 1
                    remove_city_list.append(node)
                if num_c == 0:
                    break
        # H.remove_edge(cutset[len(cutset)-1][0], cutset[len(cutset)-1][1])

        # Deal with the 2 partition of graphs and new s, t
        # Say we partition a graph S---Split--Split----T
        # Then We need S_list and T_list to be S---T--S----T
        # S-----T--S---SPlit---SPLIT---T
        # S-----T--S----T------S-----T
        # We need to keep edge to not disconnect graph
        # PARTITION STEP BROKEN FIX THIS
        remaining_edge = cutset[len(cutset) - 1]
        s_new = cutset[len(cutset) - 1][1]
        t_new = cutset[len(cutset) - 1][0]
        tempST = ST_pairs[partition_cnt].copy()
        copy1_lst = []
        copy2_lst = []
        for s_t in tempST:
            # print(s_t)
            if s_t[0][0] in partition[0]:
                copy1_lst.append((s_t[0][0], t_new))
            if s_t[0][1] in partition[1]:
                copy2_lst.append((s_new, s_t[0][1]))
            if s_t[0][0] in partition[0] and s_t[0][1] in partition[0]:
                copy1_lst.append((s_t[0][0], s_t[0][1]))
            if s_t[0][0] in partition[1] and s_t[0][1] in partition[1]:
                copy2_lst.append((s_t[0][0], s_t[0][1]))
        ST_pairs.append([copy1_lst, copy2_lst])
        # print(remaining_edge)
        # s_list.append(s_list[partition_cnt].copy())
        # s_list[partition_cnt+1].append(cutset[len(cutset)-1][1]) # 0 | 0,s | 0,s,sp
        # t_list.append([cutset[len(cutset)-1][0]])
        # t_list[partition_cnt+1].extend(t_list[partition_cnt])
        partition_cnt += 1
        # print("remove edge list: ", remove_edge_list)
        # print("remove city list: ", remove_city_list)
        # print("new shortest path is:", nx.algorithms.shortest_paths.weighted.dijkstra_path(H, 0, len(G)-1), "with weight: ", nx.dijkstra_path_length(H, 0, len(G)-1)
    return remove_edge_list, remove_city_list


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs/small-1.out')

# if __name__ == '__main__':
# 	inputs = glob.glob('inputs/medium/*')
# 	for input_path in inputs:
# 		output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
# 		G = read_input_file(input_path)
# 		c, k = solve(G)
# 		assert is_valid_solution(G, c, k)
# 		distance = calculate_score(G, c, k)
# 		print(distance)
# 		write_output_file(G, c, k, output_path)

if __name__ == '__main__':
    inputs = sorted(glob.glob('inputs/medium/*')) #change this
    new = open("new_distances.txt", "w")
    short = open("shortest_distances_medium.txt", "r") #change this
    delta = open("delta_distances.txt", "w")
    delta_dist_array = []
    heur_count = {1:0, 2:0, 3:0, 4:0, 5:0}
    for input_path in inputs:
        output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        c, k, best = solve2(G)
        heur_count[best] = heur_count[best] + 1
        assert is_valid_solution(G, c, k)
        b = calculate_score(G, c, k)
        distance = b
        new.write(input_path.split("/")[2] + ": " + str(distance) + "\n")
        print(basename(normpath(input_path))[:-3] + ": " + str(distance))
        print(heur_count)
        delta_dist_array.append(distance)
        write_output_file(G, c, k, output_path)
    new.close()
    average = delta_dist_array[:]
    count_better = 0
    count_worse = 0
    count_same = 0
    i = 0
    for line in short:
        old_score = float(line.split(": ")[1][:-1])
        delta_dist_array[i] = delta_dist_array[i] - old_score
        average[i] = (average[i] - old_score) / old_score
        if delta_dist_array[i] > 0:
            delta.write(line.split(": ")[0] + ": " + str(delta_dist_array[i]) + " better" "\n")
            count_better += 1
        elif delta_dist_array[i] < 0:
            delta.write(line.split(": ")[0] + ": " + str(delta_dist_array[i]) + " worse" "\n")
            count_worse += 1
        else:
            delta.write(line.split(": ")[0] + ": " + str(delta_dist_array[i]) + " same" "\n")
            count_same += 1
        i += 1
    delta.write("number better: " + str(count_better) + "\n")
    delta.write("number worse: " + str(count_worse) + "\n")
    delta.write("number same: " + str(count_same) + "\n")
    # delta.write("average: " + str(np.mean(average)) + "\n")
    short.close()
    print(np.mean(average))
    print(heur_count)





# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == "__main__":
#     inputs = glob.glob("inputs/large/*")
#     inputs = sorted(inputs)
#     os.rename("current_distances.txt", "old_distances.txt")
#     curr = open("current_distances.txt", "w")
#     # short = open("shortest_distances.txt", "w")
#     delta = open("delta_distances.txt", "w")
#     old = open("old_distances.txt", "r")
#     delta_dist_array = []
#     for input_path in inputs:
#         output_path = "outputs/" + basename(normpath(input_path))[:-3] + ".out"
#         G = read_input_file(input_path)
#         c, k = solve2(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         curr.write(input_path.split("/")[2] + ": " + str(distance) + "\n")
#         # short.write(input_path.split("/")[2] + ": " + str(shortest) + "\n")
#         delta_dist_array.append(distance)
#         write_output_file(G, c, k, output_path)
#     curr.close()
#     # short.close()
#     short = open("shortest_distances.txt", "r")

#     i = 0
#     for line in short:
#         old_score = float(line.split(": ")[1][:-1])
#         delta_dist_array[i] = (delta_dist_array[i] - old_score) / old_score
#         delta.write(line.split(": ")[0] + ": " + str(delta_dist_array[i]) + "\n")
#         i += 1
#     print(np.mean(delta_dist_array))
#     short.close()

    """
    shortest_path = nx.algorithms.shortest_paths.weighted.dijkstra_path(G, 0, len(G)-1)
    path_length = nx.dijkstra_path_length(G, 0, len(G)-1)
    
    #remove nodes/edges along the path to make it move somewhere else
    dists = []
    for i in range(len(shortest_path)-1):
        dists.append((H[shortest_path[i]][shortest_path[i+1]]['weight'], shortest_path[i], shortest_path[i+1]))	
    dists.sort()

    k_count = 0
    c_count = 0
    for i in range(len(dists)):
        if i >= len(dists): break
        if num_k < k_count: break
        if num_c < c_count: break
        if not nx.algorithms.shortest_paths.generic.has_path(H, 0, len(G)-1):
            print ("somehow something went wrong :C")
            break
        J = H.copy()
        prob = random.random()
        if prob > 0.5:
            J.remove_edge(dists[i][1], dists[i][2])
            if nx.algorithms.shortest_paths.generic.has_path(J, 0, len(G)-1):
                path_length_new = nx.dijkstra_path_length(J, 0, len(G)-1)
                if path_length_new > path_length:
                    H = J.copy()
                    remove_edge_list.append((dists[i][1], dists[i][2]))
                    path_length = path_length_new
                    k_count += 1
        else:
            if dists[i][1] == 0 or dists[i][1] == len(dists) -1: continue
            J.remove_node(dists[i][1])
            if nx.algorithms.shortest_paths.generic.has_path(J, 0, len(G)-1):
                path_length_new = nx.dijkstra_path_length(J, 0, len(G)-1)
                if path_length_new > path_length:
                    H = J.copy()
                    remove_city_list.append(dists[i][1])
                    path_length = path_length_new
                    dists = [(length, val, key) for (length, val, key) in dists if val == dists[i][1]]
                    c_count += 1
    # print(dists)
    #---end---
    """
