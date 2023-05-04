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


def main():
    # Time the script
    t_start = time.time()
    print(date_time.get_current_time(), "Program started")

    # Load the cleaned data
    data = g.load_pickled_data(DATA_LOC+"clean_data")
    print(date_time.get_current_time(), "Loaded clean data")

    # Create a PLG object
    PLG = plg.PLG()

    # Generate node set
    rc = node_generation(PLG, data)
    print(date_time.get_current_time(), "Generated nodes")
    g.save_pickled_data(PLG_SAVE_LOC+"PLG", PLG)
    print(date_time.get_current_time(), "Generated nodes. Saved...")

    # Generate discrete vehicle paths
    rc = get_discrete_vehicle_paths(data=data, PLG=PLG)
    print(date_time.get_current_time(), "Discretised vehicle paths")
    g.save_pickled_data(PLG_SAVE_LOC+"PLG", PLG)
    g.save_pickled_data(DATA_LOC+"clean_data", data)
    print(date_time.get_current_time(), "Discretised vehicle paths. Saved...")

    # Create the adjacency matrix
    rc = adj_mat_generation(PLG)
    print(date_time.get_current_time(), "Adjacency matrix generated")
    g.save_pickled_data(PLG_SAVE_LOC+"PLG", PLG)
    print(date_time.get_current_time(), "Adjacency matrix generated. Saved...")

    # Get the start and target node clusters
    rc = cluster_generation(PLG)
    print(date_time.get_current_time(), "Start/target node clusters generated")
    g.save_pickled_data(PLG_SAVE_LOC+"PLG", PLG)
    print(date_time.get_current_time(), "Start/target node clusters generated. Saved...")

    # Generate the travel dictionary
    rc = travel_dict_generation(PLG)
    print(date_time.get_current_time(), "Travel dictionary generated")
    g.save_pickled_data(PLG_SAVE_LOC+"PLG", PLG)
    print(date_time.get_current_time(), "Travel dictionary generated. Saved...")

    # Print time take
    print(f"PLG generation time taken = {round(time.time() - t_start, 3)} s")


if __name__=="__main__":
    main()

