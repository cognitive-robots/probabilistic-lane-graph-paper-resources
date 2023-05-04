import numpy as np
import functions.general as g


###############################################################################
# adj_mat_generation:                                                         #
#                                                                             #                             
# Purpose: Generate the adjacency matrix for the PLG using the discrete       #
#          vehicle paths dictionary. We increment the [ii,jj] matrix entry if #
#          a vehicle went from node ii to node jj in its path. Therefore, the #
#          adjacency matrix will be directed. If the [ii,jj] entry is 0 then  #
#          there is no edge between nodes ii and jj, otherwise there is an    #
#          edge and the value of the entry is the number of times that edge   #
#          was traversed by vehicles in the dataset.                          #    
#                                                                             #                                    
# Params IN/OUT PLG  - A PLG object of type "PLG" defined in classes/PLG.py.  #
#                      The PLG.adjmat parameter will be updated with the 2D   #
#                      numpy array.                                           #
#                                                                             #
###############################################################################
def adj_mat_generation(PLG):
    # Initialisations
    discrete_vehicle_paths = PLG.vehicle_paths
    PLG.adjmat = np.zeros((PLG.num_nodes, PLG.num_nodes))

    # Cycle through the discrete vehicle paths and create edges between any two
    # adjacent nodes in a vehicle path
    for ii in discrete_vehicle_paths:
        # Path as a list of nodes
        path = discrete_vehicle_paths[ii]
        path_length = len(path)

        # Cycle through the vehicle path
        for jj in range(path_length - 1):
            current_node = path[jj]
            next_node = path[jj + 1]

            # Create an edge between these two nodes, we're going from
            # current_node->next node so we will only increment the row/col
            # corresponding to [current_node, next_node]. This means that the
            # directions in our adjacency matric are as follows:
            # current_node = row
            # nect_node = column
            # So an edge goes from the row to the column
            PLG.adjmat[current_node, next_node] += 1

    # Convert the adjacency matrix to a probability matrix by cylcing through
    # each row and dividing each entry by the sum of the row
    PLG.adjmat = g.normalise_matrix_rows(PLG.adjmat)

    return True


    




