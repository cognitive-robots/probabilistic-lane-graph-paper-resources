###############################################################################
# This file contains the PLG class, which is used to store the PLG data.      #
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

