import sys
import os

# On my machine I need this line otherwise I get a "ModuleNotFoundError" when
# trying to import the other modules I have written within this directory.
sys.path.append(os.getcwd())

import functions.general as g
import functions.date_time as date_time
import functions.graph as graph
import classes.PLG as plg
import time
import numpy as np
from inputs import *
import matplotlib.pyplot as plt


DATA_LOC = "data/"+DATASET+"/cleaned/"
PLG_SAVE_LOC = "data/"+DATASET+"/data-structures/"


def main():
    # Time the script
    t_start = time.time()
    print(date_time.get_current_time(), "Program started")

    # Create a PLG object
    PLG = g.load_pickled_data(PLG_SAVE_LOC+"PLG")
    print(date_time.get_current_time(), "Loaded PLG")

    # Now generate the path
    len_of_path = 300
    while (len_of_path == 300) or (len_of_path < 5):
        # Generate a random path using our path planning algorithm and plot it.
        # First generate a random starting cluster, then choose a random start
        # node from that cluster, then generate a random target cluster
        start_cluster = np.random.choice(list(PLG.start_clusters.keys()))
        start_node = np.random.choice(PLG.start_clusters[start_cluster])
        target_cluster = np.random.choice(list(PLG.target_clusters.keys()))
        path = graph.path_generation(PLG, start_node, target_cluster)
        len_of_path = len(path)
    print(date_time.get_current_time(), "Generated a random path")

    # Get the output data matrix
    output_data = graph.node_path_to_output_data(PLG, path)

    # Save the output data to a file called "output_data_<path length>"
    np.savetxt(PLG_SAVE_LOC+"output_data_"+str(len_of_path), output_data, fmt="%f")


if __name__=="__main__":
    main()

