import sys
import os

# On my machine I need this line otherwise I get a "ModuleNotFoundError" when
# trying to import the other modules I have written within this directory.
sys.path.append(os.getcwd())

import functions.general as g
import functions.date_time as date_time
import functions.graph as graph
import time
import matplotlib.pyplot as plt
import random
from inputs import *
import numpy as np


DATA_LOC = "data/"+DATASET+"/cleaned/"
PLG_SAVE_LOC = "data/"+DATASET+"/data-structures/"
COLOUR_LOWER = 0
COLOUR_UPPER = 1


class PLGVisualisationParams:
    def __init__(self, data) -> None:
        # PLG params
        self.plot_plg = PLOT_PLG
        # Background data params
        self.plot_background_data = PLOT_BACKGROUND_DATA
        self.colour_of_background_data = COLOUR_OF_BACKGROUND_DATA
        self.colour_code_lanes_in_background_data = COLOUR_CODE_LANES_IN_BACKGROUND_DATA
        # Vehicle path params
        self.plot_random_vehicle_path = PLOT_RANDOM_VEHICLE_PATH
        self.plot_discrete_path = PLOT_DISCRETE_PATH
        self.plot_average_discrete_path = PLOT_AVERAGE_DISCRETE_PATH
        self.plot_continuous_path = PLOT_CONTINUOUS_PATH
        # Generated path params
        self.plot_start_and_target_clusters = PLOT_START_AND_TARGET_CLUSTERS
        self.plot_random_generated_path = PLOT_RANDOM_GENERATED_PATH
        # Conditional params
        if self.colour_code_lanes_in_background_data:
            self.colour_of_background_data = self.generate_lane_colours_for_background_data(data)

    # Function to generate the colours (in RGB format) for the background data.
    def generate_lane_colours_for_background_data(self, data):
        lane_colour_dict = {}
        lane_colour_list = [0 for ii in range(data.num_data_points)]

        # Generate a random tuple of three value for each lane ID
        for lane_id in data.lane_sese[:,0]:
            if self.colour_code_lanes_in_background_data:
                lane_colour_dict[lane_id] = (random.uniform(COLOUR_LOWER,COLOUR_UPPER), random.uniform(COLOUR_LOWER,COLOUR_UPPER), random.uniform(COLOUR_LOWER,COLOUR_UPPER))
            else:
                lane_colour_dict[lane_id] = (0, 0, 0)

        # Now generate a list of colours corresponding to each lane ID
        for ii in range(data.num_data_points):
            lane_colour_list[ii] = lane_colour_dict[data.lane_id[ii]]

        return lane_colour_list
            

def main():
    # Time the script
    t_start = time.time()
    print(date_time.get_current_time(), "Program started")

    # Load the cleaned data
    data = g.load_pickled_data(DATA_LOC+"clean_data")
    print(date_time.get_current_time(), "Loaded clean data")

    # Create a PLG object
    PLG = g.load_pickled_data(PLG_SAVE_LOC+"PLG")
    print(date_time.get_current_time(), "Loaded PLG")

    # Get the visualisation parameters
    vis_params = PLGVisualisationParams(data)

    # Choose a random vehicle path to plot
    if vis_params.plot_random_vehicle_path:
        print(date_time.get_current_time(), f"Generating random vehicle path to plot")

        # Get the vehicle ID
        if type(vis_params.plot_random_vehicle_path) == int:
            # We have supplied a specific vehicle ID whose path we want to plot
            vehicle_id = vis_params.plot_random_vehicle_path
        else:
            # We want to plot a random vehicle path
            vehicle_id = np.random.choice(data.vehicle_sese[:,0])

        # Print the vehicle ID so we know which one we are plotting. If we find
        # an interesting path we can remember the ID and plot it again later.
        print(date_time.get_current_time(), f"Vehicle ID = {vehicle_id}")

        # Get continuous path
        x_cont = g.se_extraction(vehicle_id, data.x, data.vehicle_sese)
        y_cont = g.se_extraction(vehicle_id, data.y, data.vehicle_sese)
        # Get discrete path
        n_path = g.se_extraction(vehicle_id, data.node, data.vehicle_sese).astype(int)
        x_disc = PLG.nodes[n_path, 0]
        y_disc = PLG.nodes[n_path, 1]
        # Get average discrete path
        moving_avg_window = 5
        x_avg_disc, _ = g.moving_average(x_disc, n=moving_avg_window)
        y_avg_disc, _ = g.moving_average(y_disc, n=moving_avg_window)

    # Print time take
    print(f"Time taken to load data = {round(time.time() - t_start, 3)} s")

    # PLOTS
    if vis_params.plot_background_data:
        # Plot the entire dataset in the background
        plt.scatter(data.x, data.y, color=vis_params.colour_of_background_data, s=1, zorder=0)

    if vis_params.plot_plg:
        # Plot the PLG   
        graph.draw(PLG)

    if vis_params.plot_random_vehicle_path:
       # Plot the discrete path
        if vis_params.plot_discrete_path:
            plt.plot(x_disc, y_disc, color="orange", linestyle="-", linewidth=2, zorder=6, label="Discrete path")

        # Plot the average discrete path
        if vis_params.plot_average_discrete_path:
            plt.plot(x_avg_disc, y_avg_disc, color="green", linestyle="--", linewidth=1, zorder=7, label=f"{moving_avg_window} Point mov-avg discrete path")

        # Plot the continuous path
        if vis_params.plot_continuous_path:
            plt.plot(x_cont, y_cont, color="red", linestyle="--", linewidth=1, zorder=8, label="Continuous path")
        plt.legend()

    if vis_params.plot_start_and_target_clusters:
        # Plot the start and target clusters
        # First plot the nodes
        s_size = 7.5
        z_ord = 10
        for start_cluster in PLG.start_clusters:
            plt.scatter(PLG.nodes[PLG.start_clusters[start_cluster],0], PLG.nodes[PLG.start_clusters[start_cluster],1], color="green", s=s_size, zorder=z_ord)

        for target_cluster in PLG.target_clusters:
            plt.scatter(PLG.nodes[PLG.target_clusters[target_cluster],0], PLG.nodes[PLG.target_clusters[target_cluster],1], color="red", s=s_size, zorder=z_ord)

        # Now plot the cluster centres
        s_size = 50
        z_ord = 11
        plt.scatter(PLG.start_cluster_centres[:,0], PLG.start_cluster_centres[:,1], color="blue", marker="x", s=s_size, zorder=z_ord, label="Entry points")
        plt.scatter(PLG.target_cluster_centres[:,0], PLG.target_cluster_centres[:,1], color="magenta", marker="x", s=s_size, zorder=z_ord, label="Exit points")
        plt.legend()


    if vis_params.plot_random_generated_path:
        # Generate a random path using our path planning algorithm and plot it.
        # First generate a random starting cluster, then choose a random start
        # node from that cluster, then generate a random target cluster
        start_cluster = np.random.choice(list(PLG.start_clusters.keys()))
        start_node = np.random.choice(PLG.start_clusters[start_cluster])
        target_cluster = np.random.choice(list(PLG.target_clusters.keys()))
        
        # Now generate the path
        path = graph.path_generation(PLG, start_node, target_cluster)

        # Plot the path
        plt.plot(PLG.nodes[path,0], PLG.nodes[path,1], color="orange", linestyle="-", linewidth=1.5, zorder=12, label="Randomly generated path")
        plt.legend()

    # Set the aspect ratio to be equal
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()


if __name__=="__main__":
    main()

