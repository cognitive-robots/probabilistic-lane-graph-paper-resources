###############################################################################
# This file contains all of the inputs the user may modify for the PLG        #
# generation and visualisation code.                                          #
#                                                                             #
# The inputs will be split into three sections:                               #
# 1. Dataset                                                                  #
# 2. PLG generation                                                           #
# 3. PLG visualisation                                                        #
#                                                                             #
# All inputs are provided in the variables below. If any of the inputs are    #
# modified, the user must ensure that the valid script is (re)run in order    #
# for the changes to take effect.                                             #
###############################################################################

###############################################################################
# Dataset to use                                                              #
#                                                                             #
# Relevant script: - data-processing\data_cleaner.py                          #
#                  - Run this script to generate the cleaned data from the    #
#                    raw data. This script should only have to be run once as #
#                    the cleaned data is not modified by any other scripts.   #
#                  - This script shouldn't need to be run for the default     #
#                    datasets as the cleaned data is already provided. If the #
#                    user would like to use their own dataset, they must      #
#                    ensure that the data is cleaned before running any of    #
#                    the other scripts.                                       #
#                                                                             #
# Purpose: Specify the dataset to use. We have provided a single dataset      #
#          which is readily available in the data folder. This datasets has   #
#          already been cleaned and is ready to be used. If you would like to #
#          use your own dataset, you can add it to the "data" folder and then #
#          specify the name of the subfolder here. In order to use a custom   #
#          dataset, you must ensure that the data contains the following      #
#          files:                                                             #
#                                                                             #
#          Global_X   - The global x coordinates of the vehicles.             #
#          Global_Y   - The global y coordinates of the vehicles.             #
#          Vehicle_ID - An integer which can uniquely identify different      #
#                         vehicles.                                           #                                            
#                                                                             #
# Params:  DATASET - The dataset to use. This string should take the name of  #
#                    the subfolder in "data" which contains the dataset. The  #
#                    default options readily available are:                   #
#                    "lankershim" - The Lankershim dataset. Units are in      #
#                                   feet.                                     #
#          UNIT:   - The units of the spatial coordinates in the dataset. In  #
#                    the PLG generation process we specify the minimum        #
#                    distance between nodes. This distance is specified in    #
#                    metres. As a result, we must ensure that the spatial     #
#                    coordinates in the dataset are also in metres. The       #
#                    options which have been built into this codebase are:    #
#                    "feet"                                                   #
#                    "metres"                                                 #
#                    Other units can be added by modifying the code in the    #
#                    classes/data.py file and re-running the data cleaner     #
#                    script.                                                  #
#                                                                             #
###############################################################################
DATASET = "Lankershim"
UNIT = "feet"

###############################################################################
# PLG generation                                                              #
#                                                                             #
# Relevant script: - plg-generation\plg_generation.py                         #
#                  - Run this script to generate the PLG data structure. If   #
#                    the user modifies any of the inputs below, they must     #
#                    ensure that this script is (re)run in order for the      #
#                    changes to take effect.                                  #
#                                                                             #
# Purpose: Specify the parameters for the PLG generation process. The PLG     #
#          generation script will generate a data structure which contains    #
#          all of the information required to visualise the PLG. The PLG data #
#          structure is stored in the data/<dataset name>/data-structures     #
#          folder. The data structure is defined in the Python script located #
#          at classes/PLG.py. NOTE: The following parameters have been tuned  #
#          to generate a PLG which is similar to the road network in the      #
#          Lankershim dataset.                                                #
#                                                                             #
# Params:  MIN_DIST_BETWEEN_NODES - The minimum distance between nodes in the #
#                                   PLG. This is specified in metres.         #
#          NUM_START_CLUSTERS     - The number of entry points in the map     #
#                                   which correspond to a cluster of nodes in #
#                                   the PLG.                                  #
#          NUM_TARGET_CLUSTERS    - The number of exit points in the map      #
#                                   which correspond to a cluster of nodes in #
#                                   the PLG.                                  #
#          DO_KMEANS              - Boolean value. Set to True if you would   #
#                                   like to use the K-Means algorithm to even #
#                                   out the distribution of nodes along the   #
#                                   lanes in the PLG.                         #
#                                   NOTE: This boolean should be set to False #
#                                   if there are no lane IDs in the dataset.  # 
#                                   NOTE: This step generally performs better #
#                                   when there are a large (enough) number of #
#                                   nodes in the PLG.                         #
#                                                                             #
###############################################################################
MIN_DIST_BETWEEN_NODES = 3
NUM_START_CLUSTERS = 10
NUM_TARGET_CLUSTERS = 10
DO_KMEANS = True

###############################################################################
# PLG visualisation                                                           #
#                                                                             #
# Relevant script: - plg-visualisation\plg_visualisation.py                   #
#                  - Run this script to visualise the PLG. If the user would  #
#                    like to modify any of the inputs below, they must ensure #
#                    that this script is (re)run in order for the changes to  #
#                    take effect.                                             #
#                                                                             #
# Purpose: Specify the parameters for the PLG visualisation produced using    #
#          the matplotlib library. We've defaulted these parameters to only   #
#          show the PLG, without any background and colour coding as this is  #
#          the fastest. However, you can change these parameters to show the  #
#          background data and colour code the PLG for a more detailed        #
#          visualisation.                                                     #
#                                                                             #
# Plot params:                                                                #
#          PLOT_PLG             - Set to True if you would like to show the   #
#                                 plot of the PLG. The boolean decides        #
#                                 whether or not to run the plt.show()        #
#                                 command.                                    #  
#          PLOT_BACKGROUND_DATA - Boolean value. Set to True if you would     #
#                                 like to plot the original dataset in the    #
#                                 background. Doing this allows us to         #
#                                 visually compare the PLG to the actual road #
#                                 network. Defaults to False because setting  #
#                                 this to True can slow the rendering of the  #
#                                 plot.                                       #
#          COLOUR_OF_BACKGROUND_DATA                                          #
#                               - String to specify the colour of the         #
#                                 background data. Defaults to "grey".        #
#          COLOUR_CODE_LANES_IN_BACKGROUND_DATA                               #
#                               - Boolean value. Set to True if you would     #
#                                 like to colour code the background data     #
#                                 based on the lane ID. Each lane ID will be  #
#                                 assigned a unique colour. We generate a     #
#                                 random colour for each lane ID so each time #
#                                 the code is run, the colours will be        #
#                                 different. Defaults to False because        #
#                                 setting this to True can slow the rendering #
#                                 of the plot. NOTE: If the dataset does not  #
#                                 contain lane IDs, then we generate an array #
#                                 of zeros for the lane IDs. This means that  #
#                                 all of the background data will be the same #
#                                 colour. In our dataset, the lane IDs are    #
#                                 only available for the Lankershim dataset.  #
#                                                                             #
# Node params:                                                                #
#          NODE_SIZE            - The size of the nodes in the PLG.           #
#          NODE_COLOUR          - The colour of the nodes in the PLG.         #
#          COLOUR_CODE_LANES_IN_PLG                                           #
#                               - Boolean value. Set to True if you would     #
#                                 like to colour code the nodes in the PLG    #
#                                 based on the lane ID, similar to the        #
#                                 background data.                            #
#                                                                             #
# Edge params:                                                                #
#          EDGE_COLOUR          - The colour of the edges in the PLG.         #
#          EDGE_LINE_WIDTH      - The line width of the edges in the PLG.     #
#          SHADE_EDGES_WITH_CONNECTION_PROBABILITY                            #
#                               - Boolean value. Set to True if you would     #
#                                 like to shade the edges in the PLG based    #
#                                 on the connection probability. A darker     #
#                                 shade of the edge colour would indicate a   #
#                                 higher connection probability. Defaulted to #
#                                 True.                                       #
#                                                                             #
# Node label params:                                                          #
#          NODE_LABELS          - Value to specify whether or not to show the #
#                                 node labels. This variable can take the     # 
#                                 following values:                           #
#                                 None       - Don't show node labels.        #
#                                 "node_id"  - Show the node ID.              #
#                                 "lane_id"  - Show the lane ID of each node. #
#                                 array_like - An array of strings which      #
#                                              specify the labels to show.    #
#                                              The string in position i of    #
#                                              the array will be the label    #
#                                              for node i.                    #
#          NODE_LABELS_FONT_SIZE                                              #
#                               - The font size of the node labels.           #
#          NODE_LABELS_FONT_COLOUR                                            #
#                               - The font colour of the node labels.         #
#                                                                             #
# Path params:                                                                #
#          PLOT_RANDOM_VEHICLE_PATH                                           #
#                               - Boolean value. Set to True if you would     #
#                                 like to plot a random vehicle path. Or, set #
#                                 to an integer value. If this is an integer  #
#                                 value, then the value specifies the ID of   #
#                                 the vehicle whose path you would like to    #
#                                 plot. If this is set to False, then no      #
#                                 vehicle path will be plotted.               #
#          PLOT_CONTINUOUS_PATH - Boolean value. Set to True if you would     #
#                                 like to plot the continuous path of the     #
#                                 vehicle. "Continuous" in this case refers   #
#                                 the original path of the vehicle in the     #
#                                 dataset.                                    #                                              
#          PLOT_DISCRETE_PATH   - Boolean value. Set to True if you would     #
#                                 like to plot the discrete path of the       #
#                                 vehicle. "Discrete" in this case refers     #
#                                 to the path of the vehicle in the PLG.      #
#          PLOT_AVERAGE_DISCRETE_PATH                                         #
#                               - Boolean value. Set to True if you would     #
#                                 like to plot the average discrete path of   #
#                                 the vehicle. "Average discrete" in this     #
#                                 case refers to a moving average of the node #
#                                 path of the vehicle through the PLG.        #
#                                                                             #
# Path generation params:                                                     #
#          PLOT_RANDOM_GENERATED_PATH                                         #
#                              - Boolean value. Set to True if you would to   #
#                                plot a random path from an entry point in    #
#                                map to an exit. The path is generated using  #
#                                using our data driven path planning          #
#                                algorithm.                                   #
#          PLOT_START_AND_END_NODES                                           #
#                              - Boolean value. Set to True if you would to   #
#                                plot all of the start and end nodes in the   #
#                                PLG to visualise the entry and exit points.  #                                              
#                                                                             #
###############################################################################
PLOT_PLG = True
PLOT_BACKGROUND_DATA = False
COLOUR_OF_BACKGROUND_DATA = "grey"
COLOUR_CODE_LANES_IN_BACKGROUND_DATA = False

NODE_SIZE = 5
NODE_COLOUR = "black"
COLOUR_CODE_LANES_IN_PLG = False

EDGE_COLOUR = "black"
EDGE_LINE_WIDTH = 0.75
SHADE_EDGES_WITH_CONNECTION_PROBABILITY = True

NODE_LABELS = None
NODE_LABELS_FONT_SIZE = 6
NODE_LABELS_FONT_COLOUR = "red"

PLOT_RANDOM_VEHICLE_PATH = False
PLOT_CONTINUOUS_PATH = True
PLOT_DISCRETE_PATH = True
PLOT_AVERAGE_DISCRETE_PATH = True

PLOT_RANDOM_GENERATED_PATH = True
PLOT_START_AND_TARGET_CLUSTERS = False

                                                                            
