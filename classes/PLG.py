###############################################################################
# This file contains the PLG class, which is used to store the PLG data.      #
#                                                                             #
# Params:                                                                     #
#                                                                             #
# num_nodes                - Number of nodes in the PLG.                      #
# nodes                    - A 2D numpy array of the [x,y] node coordinates.  #
# node_lane_ids            - The i'th entry contains the lane ID for the node #
#                            i.                                               #
# vehicle_paths            - A dictionary of {vehicle ID : node path}         #
# adjmat                   - A 2D numpy adjacency matrix populated with the   #
#                            connection probability.                          #
# start_cluster_centres    - A 2D numpy matrix of [x,y] coordinates. The i'th #
#                            row contains the i'th row contains the           #
#                            coordinates for cluster i.                       #
# target_cluster_centres   - Similar to above but for target clusters.        #
# start_clusters           - A dictionary of {cluster id : [list of nodes]}.  #
# target_clusters          - Similar to above but for target clusters.        #
# closest_clusters_dict    - A dictionary of {cluster id : [list of cluster   #
#                            IDs]}. Where the list of cluster IDs is ordered  #
#                            from lowest to highest with respect to their     #
#                            distance from the key value.                     #
# p_next_node              - A 2D numpy adjacency matrix populated with the   #
#                            connection probability.                          #
# p_next_node_given_target - A 2D numpy adjacency matrix populated with the   #
#                            connection probability. However, this matrix is  #
#                            built from vehicles which all had the same       #
#                            target cluster as their destination.             #
#                                                                             #
###############################################################################
class PLG:
    def __init__(self) -> None:
        self.num_nodes = None
        self.nodes = None
        self.node_lane_ids = None
        self.vehicle_paths = None
        self.adjmat = None
        self.start_cluster_centres = None
        self.target_cluster_centres = None
        self.start_clusters = None
        self.target_clusters = None
        self.closest_clusters_dict = None
        self.p_next_node = None
        self.p_next_node_given_target = None

