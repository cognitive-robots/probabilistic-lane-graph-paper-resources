import sys
import os

# On my machine I need this line otherwise I get a "ModuleNotFoundError" when
# trying to import the other modules I have written within this directory.
sys.path.append(os.getcwd())

import functions.general as g
import functions.date_time as date_time
import classes.PLG as plg
import time
from inputs import *

# Import functions for PLG generation
from node_generation import node_generation
from get_discrete_vehicle_paths import get_discrete_vehicle_paths
from adj_mat_generation import adj_mat_generation
from cluster_generation import cluster_generation
from travel_dict_generation import travel_dict_generation


DATA_LOC = "data/"+DATASET+"/cleaned/"
PLG_SAVE_LOC = "data/"+DATASET+"/data-structures/"

PLG_SAVE_NAME = "PLG"
DATA_SAVE_NAME = "clean_data_v2"


def main():
    # Time the script
    t_start = time.time()
    print(date_time.get_current_time(), "Program started")

    # Load the cleaned data
    data = g.load_pickled_data(DATA_LOC+DATA_SAVE_NAME)
    print(date_time.get_current_time(), "Loaded clean data")

    # Create a PLG object
    PLG = plg.PLG()

    # Generate node set
    rc = node_generation(PLG, data)
    print(date_time.get_current_time(), "Generated nodes")

    # Generate discrete vehicle paths
    rc = get_discrete_vehicle_paths(data=data, PLG=PLG)
    print(date_time.get_current_time(), "Discretised vehicle paths")

    # Create the adjacency matrix
    rc = adj_mat_generation(PLG)
    print(date_time.get_current_time(), "Adjacency matrix generated")

    # Get the start and target node clusters
    rc = cluster_generation(PLG)
    print(date_time.get_current_time(), "Start/target node clusters generated")

    # Generate the travel dictionary
    rc = travel_dict_generation(PLG)
    print(date_time.get_current_time(), "Travel dictionary generated")

    # Save and print time taken
    g.save_pickled_data(PLG_SAVE_LOC+PLG_SAVE_NAME, PLG)
    g.save_pickled_data(DATA_LOC+DATA_SAVE_NAME, data)
    print(date_time.get_current_time(), "Saved PLG and updated clean_data with node inforamtion")
    print(f"PLG generation time taken = {round(time.time() - t_start, 3)} s")


if __name__=="__main__":
    main()

