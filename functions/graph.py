import numpy as np
import matplotlib.pyplot as plt
import random
from math import inf
from inputs import *
import copy


COLOUR_LOWER = 0
COLOUR_UPPER = 1


class GraphPlotInformation:
    def __init__(self, PLG) -> None:
        # Node params
        self.node_size = NODE_SIZE
        self.node_colour = NODE_COLOUR
        self.colour_code_lanes_in_plg = COLOUR_CODE_LANES_IN_PLG
        # Edge params
        self.edge_line_width = EDGE_LINE_WIDTH
        self.edge_colour = EDGE_COLOUR
        # Edge shading params
        self.shade_edges_with_connection_probability = SHADE_EDGES_WITH_CONNECTION_PROBABILITY
        self.shade_darkness = 0.8
        # Node label params
        self.node_labels = NODE_LABELS
        self.node_labels_font_size = NODE_LABELS_FONT_SIZE
        self.node_labels_font_colour = NODE_LABELS_FONT_COLOUR
        # Conditonal params
        if self.colour_code_lanes_in_plg:
            self.node_colour = self.generate_colours_for_lane_ids(PLG)
        if self.node_labels is not None:
            self.node_labels = self.generate_node_labels(PLG)

    def generate_colours_for_lane_ids(self, PLG):
        lane_colour_dict = {}
        lane_colour_list = [0 for ii in range(PLG.num_nodes)]
        lane_ids = list(set(PLG.node_lane_ids))

        # Generate a colour (random tuple) of three value for each lane ID
        for lane_id in lane_ids:
            lane_colour_dict[lane_id] = (random.uniform(COLOUR_LOWER,COLOUR_UPPER), random.uniform(COLOUR_LOWER,COLOUR_UPPER), random.uniform(COLOUR_LOWER,COLOUR_UPPER))

        # Now create a list of colours corresponding to each lane ID
        for ii in range(PLG.num_nodes):
            lane_colour_list[ii] = lane_colour_dict[PLG.node_lane_ids[ii]]

        return lane_colour_list
    
    def generate_node_labels(self, PLG):
        # Get a vector of node labels
        if self.node_labels == "node_id":
            return [str(ii) for ii in range(PLG.num_nodes)]
        elif self.node_labels == "lane_id":
            return [str(PLG.node_lane_ids[ii]) for ii in range(PLG.num_nodes)]
        else:
            return self.node_labels


def draw(PLG):
    """Draws the PLG object.
    """
    # Initialise Graph Plot Information
    graph_plot_info = GraphPlotInformation(PLG)
    # Coordinates of nodes
    x = PLG.nodes[:,0]
    y = PLG.nodes[:,1]
    # Adjacency matrix
    adj_mat = PLG.adjmat

    # Get the shape of the adjacency matrix and assert that it is square
    shape_of_adj_mat = np.shape(adj_mat)
    num_rows = shape_of_adj_mat[0]
    num_cols = shape_of_adj_mat[1]
    assert num_rows == num_cols

    # Cycle through the adjacency matrix and plot edges
    for ii in range(num_rows):
        for jj in range(ii+1, num_cols):
            if max(adj_mat[ii,jj], adj_mat[jj,ii]) > 0:
                # If we've decided to shade the edges by probability then get
                # the shading for this edge
                if graph_plot_info.shade_edges_with_connection_probability:
                    shade_value = min(1 - adj_mat[ii, jj], 1 - adj_mat[jj, ii])*graph_plot_info.shade_darkness
                    graph_plot_info.edge_colour = [shade_value, shade_value, shade_value]

                # Plot the edge
                plt.plot([x[ii], x[jj]], [y[ii], y[jj]], color=graph_plot_info.edge_colour, linewidth=graph_plot_info.edge_line_width, zorder=3)

    # Plot the graph nodes
    plt.scatter(x, y, color=graph_plot_info.node_colour, s=graph_plot_info.node_size, zorder=4)

    # Plot the node labels
    if graph_plot_info.node_labels is not None:
        # Offset the labels slightly so that they are not plotted directly on
        # top of the nodes
        dx = 0.5
        dy = 0.5
        for ii in range(PLG.num_nodes):
            plt.text(x[ii] + dx, y[ii] + dy, graph_plot_info.node_labels[ii], color=graph_plot_info.node_labels_font_colour, fontsize=graph_plot_info.node_labels_font_size, fontweight="bold", zorder=5)


def arg_max_p_next_node(p_next_node, current_node):
    """Returns the next node with the highest probability of being visited
    given the current node"""
    if np.sum(p_next_node[current_node,:]) == 0:
        return False
    else:
        return np.argmax(p_next_node[current_node,:])


def arg_max_p_next_node_given_target(p_next_node_given_target, closest_clusters_list, current_node):
    """Returns the next node with the highest probability of being visited
    given the current node and the target cluster. If we cannot find a next
    node given the target cluster then we will search for a next node given the
    next closest cluster, and so on."""
    for target_cluster in closest_clusters_list:
        next_node = arg_max_p_next_node(p_next_node_given_target[target_cluster], current_node)
        if next_node:
            return next_node
    

def path_generation(PLG, start_node, target_cluster):
    """Generates a path from the start node to the target cluster. If we reach
    a dead end then we will return a path that ends with "None"."""
    # Initialise the path
    path = [start_node]
    closest_clusters_list = PLG.closest_clusters_dict[target_cluster]
    max_path_length = 300
    
    # Create copies of the transition matrices
    p_next_node_given_target = copy.deepcopy(PLG.p_next_node_given_target)

    # Continue to add nodes to the path until we reach the target cluster. If
    # We add "None" to the path then we have reached a dead end and should
    # stop. I.e. we have reached a node that has no outgoing edges.
    while (path[-1] not in PLG.target_clusters[target_cluster]) and \
          (len(path) < max_path_length) and \
          (path[-1] != None):
        # Get the next node
        next_node = arg_max_p_next_node_given_target(p_next_node_given_target, closest_clusters_list, path[-1])
        # Add the next node to the path
        path.append(next_node)

    return path



