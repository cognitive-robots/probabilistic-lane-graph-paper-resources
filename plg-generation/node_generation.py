import numpy as np
from numpy.linalg import norm
from sklearn.cluster import KMeans
from inputs import *


###############################################################################
# node_generation:                                                            #
#                                                                             #
# Purpose: Generate a 2D numpy array of nodes that the PLG will be            #
#          constructed from. The nodes are generated by continuously adding   #
#          nodes to the node set, provided that they are sufficiently far     #
#          away from every other node in the node set under the euclidean     #
#          distance metric. The 2D numpy array of nodes will contain two      #
#          columns corresponding to the x and y coordinates of each node      #
#          respectively: [x, y]. The node ID will be the row index of the     #
#          coordinate in the 2D numpy.                                        #
#                                                                             #
# Params: IN     data - A data object of type "data" defined in               #
#                       classes/data.py which contains the cleaned dataset.   #
#         IN/OUT PLG  - A PLG object of type "PLG" defined in classes/PLG.py. #
#                       The PLG.nodes parameter will be updated with the 2D   #
#                       numpy array of nodes generated by this function.      #
#                                                                             # 
###############################################################################
def node_generation(PLG, data):
    # Initialisations
    data_x = np.array(data.x)
    data_y = np.array(data.y)
    data_lid = np.array(data.lane_id)
    node_set = np.array([[data_x[0], data_y[0]]])
    node_set_lane_ids = [data.lane_id[0]]
    max_kmeans_iterations = 100
    # Note that since the kmeans step is tailored to the lankershim dataset,
    # this parameter is hard-coded here and is specific to the lankershim
    # data.
    lids_to_ignore_for_kmeans = [0, 101]
    
    # First we will generate an initial set of nodes using the vehicle paths
    # and the pre-defined minimum node distance.
    # Note that in the definiton of our algorithm, we state that we will cycle
    # through the original dataset in chunks of "vehicle path". I.e. extract
    # the data for vehicle ID 1, cycle through this data, then vehicle ID 2
    # and so on. Since the "clean_data" data structure has already been sorted
    # into this format there is no need to think about that here, we can
    # proceed straight to cycling through the entire dataset.
    for ii in range(data.num_data_points):
        # Get the x and y coordinates for this data point
        x_ii = data_x[ii]
        y_ii = data_y[ii]
        d_ii = np.array([x_ii, y_ii])
    
        # Calculate the euclidean distance between this data point and every
        # ther node currently in the graph
        distance_to_nodes = norm(node_set - d_ii, ord=2, axis=1)
        nodes_within_min_distance = distance_to_nodes[distance_to_nodes < MIN_DIST_BETWEEN_NODES]
    
        # Check that this data point is atleast greater than our minimum
        # treshold away from every other node currently in the graph
        if len(nodes_within_min_distance) == 0:
            # This data point is sufficiently far from every node currently in
            # the PLG so append it to the node set
            node_set = np.vstack((node_set, [x_ii, y_ii]))
            node_set_lane_ids.append(int(data.lane_id[ii]))

    # Now we perform k-means clustering to even out the distribution of nodes
    # along the lanes. First convert the node_set_lane_ids to a numpy array
    # for the np.argwhere function to work.
    if (DO_KMEANS) and (DATASET == "lankershim"):
        node_set_lane_ids = np.array(node_set_lane_ids)
    
        # Get the unique lane IDs
        unique_lane_ids = np.unique(node_set_lane_ids)
    
        # Cycle through each lane ID and perform k-means clustering on the nodes
        # corresponding to that lane ID
        for lane_id in unique_lane_ids:
            if lane_id not in lids_to_ignore_for_kmeans:
                # Get nodes and original data points corresponding to this lane ID
                node_lid_idx = np.argwhere(node_set_lane_ids == lane_id)[:,0]
                data_lid_idx = np.argwhere(data_lid == lane_id)[:,0]

                # Get x and y coordinates for the nodes and original data points with
                # this lane ID
                node_lid_coords = node_set[node_lid_idx,:]
                data_lid_coords = np.array([data_x[data_lid_idx], data_y[data_lid_idx]]).T

                # Perform k-means clustering on the nodes and original data points with
                num_nodes_lid = len(node_lid_coords[:,0])
                kmeans_lid = KMeans(n_clusters=num_nodes_lid, max_iter=max_kmeans_iterations, init=node_lid_coords, n_init=1).fit(data_lid_coords)

                # Update the node set with the k-means cluster centres
                node_set[node_lid_idx,:] = kmeans_lid.cluster_centers_
    
    # Set the data into the PLG data structure
    PLG.nodes = node_set
    PLG.node_lane_ids = node_set_lane_ids
    PLG.num_nodes = len(PLG.nodes[:,0])

    return True

