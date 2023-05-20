# plg-generation

We provide the codebase for the generation of Probabilistic Lane Graphs (PLGs) from spatio-temporal vehicle data. There are four Python scripts in this codebase which are relevant to the user. A dataset has been provded in this repository and is ready to use straight away. This is the NGSIM, Lankershem dataset which can be found at the following location: https://ops.fhwa.dot.gov/trafficanalysistools/ngsim.htm.

The Python scripts which the user is required to manually run are:

# inputs.py
- This script contains all of the inputs the user can modify in order to alter the generation/visualisation of the PLG.
- All variables defined here are explained in the Python script itself.
- Once a change is made to the inputs.py file, the relevant scripts must be re-run in order for that change to be picked up.

# data_cleaner.py
- This is a script which is used to "clean" the original raw data.
- The script takes the raw data, removes any anomalous data points and saves the data to a Python data structure we've defined.
- The raw data which is read by this file must be provided in the following format: three text files where each line contains a data point. The three files are:
  - Vehicle_ID: The vehicle ID corresponding to each data point.
  - Global_X: The x position of the vehicle.
  - Global_Y: The y position of the vehicle.
- Optionally, a fourth file can be included which is used to generate more intuitive visualisations:
  - Lane_ID: The current lane ID of the current spatial position of the vehicle.
- Note: the readily provided dataset has already been cleaned so for this case the user may jump straight to running the plg_generation.py script.

# plg_generation.py
- Once the data is cleaned and saved, the plg_generation.py script needs to be run to generate the PLG for this dataset.
- This script saves the PLG in a data structure which we have defined in the "classes" folder.

# plg_visualisation.py
- Once the PLG data structure is saved for a given dataset it can be visualised using plg_visualisation.py.
- The parameters of the visualisation are contained in the inputs.py file.
- All visualisations are produced using the matplotlib library.

# single_agent.py
- A script to generate data for the path of a single agent in the absence of BVs.
- This script will save a data matrix to the same location the PLG is stored.
- The columns of the data matrix are: x coord, y coord, heading angle.

# Default parameters and outputs
In the inputs.py file we have already configured a set of parameters which produce a PLG for the Lankershim dataset. We have included the relevant raw data in the data/lankershim folder and have already cleaned the data using the data_cleaner.py script. Running plg_generation.py will then generate and save the PLG data structure for the configuration in inputs.py. The PLG output from this configuration is shown below:

<img width="294" alt="image" src="https://user-images.githubusercontent.com/102254720/236274646-6055f0c3-b591-49fe-bd8f-2c060660603a.png">

We've also provided an implementation of the path planning algorithm. If the PLOT_RANDOM_GENERATED_PATH flag is set to True then a path will be generated and plotted between a random entry point on the map to a random exit point. An example generated path is shown below:

<img width="267" alt="image" src="https://user-images.githubusercontent.com/102254720/236272942-bfa69f40-1e3a-4547-9523-f3cc1b498e05.png">


