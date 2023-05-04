# plg-generation

We provide the codebase for the generation of Probabilistic Lane Graphs (PLGs) from spatio-temporal vehicle data. There are four Python scripts in this codebase which are relevant to the user. The relevant Python scripts are:

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

# plg_generation.py
- Once the data is cleaned and saved, the plg_generation.py script needs to be run to generate the PLG for this dataset.
- This script saves the PLG in a data structure which we have defined in the "classes" folder.

# plg_visualisation.py
- Once the PLG data structure is saved for a given dataset it can be visualised using plg_visualisation.py.
- The parameters of the visualisation are contained in the inputs.py file.
- All visualisations are produced using the matplotlib library.
