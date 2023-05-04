import numpy as np
import functions.general as g
from numpy.linalg import norm
from sklearn.cluster import KMeans
from inputs import *


###############################################################################
# travel_dict_generation:                                                     # 
#                                                                             #
# Purpose: Generate the probability of transitioning from one node to another #
#          given that we know the target cluster. Therefore we will generate  #
#          a dictionary of {target cluster: transition matrix}.               #
#                                                                             #
# Params: IN/OUT PLG  - The travel dictionary will be assigned to the PLG     #
#                       PLG.p_next_node_given_target parameter.               #
#                                                                             # 
###############################################################################
def travel_dict_generation(PLG):
    p_next_node_given_target = {ii:np.zeros((PLG.num_nodes, PLG.num_nodes)) for ii in range(NUM_TARGET_CLUSTERS)}

    # Cycle through each vehicle path and update the matrices in the
    # p_next_node_given_target dict
    for ii_path in PLG.vehicle_paths:
        path = PLG.vehicle_paths[ii_path]
        num_nodes_in_path = len(path)
        target_cluster = g.get_dict_key_given_value_list_element(PLG.target_clusters, path[-1])

        # Cycle through each node in the path and update the
        # p_next_node_given_target matrix with the frequency of transitions
        # from the current node to the next node given that ww know the target
        # cluster
        for ii in range(num_nodes_in_path-1):
            current_node = path[ii]
            next_node = path[ii+1]
            p_next_node_given_target[target_cluster][current_node, next_node] += 1

    # Now we need to normalise the p_next_node_given_target matrices so that
    # each row sums to 1
    for ii in p_next_node_given_target:
        # Normalise this matrix
        p_next_node_given_target[ii] = g.normalise_matrix_rows(p_next_node_given_target[ii])

    # Assign the p_next_node_given_target matrix to the PLG object
    PLG.p_next_node_given_target = p_next_node_given_target

    return PLG


