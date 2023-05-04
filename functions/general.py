import numpy as np
import pickle


# When we index data_vec we need to go from [index_lower:index_upper + 1]
# because this is how Python indexing works. You index 1 beyond the final
# element you want to include.
ONE = 1


def save_pickled_data(fname, data_structure_to_save):
    """Save data using the pickle module

    Args:
        fname (string): Filename.
        data_structure_to_save (Python object): A Python data structure. E.g.,
            dictionary, list, custom class.
    """
    with open(fname, "wb") as handle:
        pickle.dump(data_structure_to_save, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickled_data(fname):
    """Load data using the pickle module"""
    with open(fname, "rb") as file_to_read:
        loaded_struct = pickle.load(file_to_read)
    return loaded_struct


def reorder(reorder_vector, mat_to_reorder, reverse=False):
    """Reorders the matrix "mat_to_reorder" according to the reordering indices
    of the reorder_vector (low to high). E.g, we sort "reorder_vector" from
    low-to-high (or vice versa if the "reverse" bool is set to True) and then
    we modify the "mat_to_reorder" according to this sorting.

    Args:
        reorder_vector (array): Vector to sort.
        mat_to_reorder (2D numpy array): Matrix to be reordered.
        reverse (bool, optional): Set to True if you want to sort from
            high-to-low. Defaults to False.

    Returns:
        2D numpy array: Reordered version of "mat_to_reorder".
    """
    # Turn inputs into numpy arrays
    reorder_vector = np.array(reorder_vector)
    mat_to_reorder = np.array(mat_to_reorder)
    # Gives indices of sorted vector
    sorted_indices = reorder_vector.argsort()
    # Reverse the order if needed
    if reverse == True:
        sorted_indices = np.flip(sorted_indices)
    # Reorder the matrix
    mat_to_reorder = mat_to_reorder[sorted_indices]
    return mat_to_reorder


def get_se_matrix(ids, unique_ids=False, order=True):
    """Generates a se data_vec given a list of IDs

    Args:
        ids (array): A list of (integer) IDs in which data with that common ID is
            contained in the same index in another array-like structure.
        unique_ids (bool, optional): Set to true if you want to output a sese data_vec with
            fully unique IDs. E.g, if ID "1" appears twice [S, E, S, E] then we split 
            this into two separte IDs "1" and "2" each with a single [S, E]. Defaults to
            False.
        order (bool, optional): Re-orders data_vec with increasing IDs. Defaults to True.

    Returns:
        numpy array: Numpy array describing the start-end information of the input ids.
            E.g, if we get an input ID list of [0, 0, 0, 1, 1, 2, 2, 2, 0, 0] then we will
            output a data_vec where each row as the following format:
            [id, starting_index_of_id, end_index_of_id, start_index_of_id, end_index_of_id]
            In this case there are two [start, end] pairs because the ID "0" appears twice
            in the list so we need to capture both appearances. This data_vec is useful
            to help us extract all data corresponding to a specific ID from a list of data.
            We call this data structure a "se data_vec" where "se" denotes the "start-end"
            pairs we use for referencing.
    """
    # Get [id, num_SE, S, E] for first, this will be an unordered list with repeated IDs
    id_SE = np.zeros((0, 4))
    # Initialise a dict{} to remember the frequency with which each 'id' appears
    id_freq = {}
    number_of_data_points = len(ids)
    prev_id = 'no_id_should_have_this_name'

    for k in range(number_of_data_points):
        this_id = ids[k]
        # Check if this is a new id
        if this_id != prev_id:
            # Build id_freq
            if str(this_id) in id_freq:
                id_freq[str(this_id)] += 1
            else:
                id_freq[str(this_id)] = 1

            # Build SE data_vec
            if k == 0:
                id_SE = np.vstack((id_SE, [this_id, id_freq[str(this_id)], k, 0]))
            else:
                id_SE = np.vstack((id_SE, [this_id, id_freq[str(this_id)], k, 0]))
                id_SE[-2,3] = k-1 # add 'E' of previous ID

        # Consider final element, add 'E' for final element
        if k == number_of_data_points-1:
            id_SE[-1,3] = k

        prev_id = this_id

    unique_ids = False
    if not order:
        if len(set(id_SE[:,0])) == len(id_SE[:,0]):
            unique_ids = True

    if unique_ids and not order:
        return id_SE.astype(int)
    else:
        if not order:
            print("... IDs are NOT unique for this SESE data_vec.")
        # Re order in terms of id
        id_SE_ordered = reorder(id_SE[:,0], id_SE)

        # Turn unordered id_SE data_vec into ordered id_SE_SE data_vec
        id_freq_list = list(id_freq.values())
        ordered_id_list = list(set(ids))
        SE_SE_rows, SE_SE_cols = len(id_freq_list), max(id_freq_list)
        se_mat = np.zeros((SE_SE_rows, 2 + 2*SE_SE_cols))
        n_SE = len(id_SE[:,0])

        prev_id = 'no_id_should_have_this_name'
        for k in range(n_SE):
            this_id, this_id_instance, start, end = id_SE[k,0], id_SE[k,1], id_SE[k,2], id_SE[k,3]

            i = ordered_id_list.index(this_id)

            se_mat[i, 0] = this_id
            se_mat[i, 1] += 1

            i_s, i_e = int(2*se_mat[i, 1]), int(2*se_mat[i, 1]+1)

            se_mat[i, i_s], se_mat[i, i_e] = start, end

        return se_mat.astype(int)


def se_extraction(id, data_vec, se_mat, sub_index=None, print_error=True):
    """Extracts all data with the ID "id" from "data_vec". For example,
    consider the data vector with a corresponding ID vectory as follows:

    data_vec = [d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10]
    id_vec = [0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 1]

    In this case, data entries [d0, d1, d2] correspond to the object with
    ID = 0, [d2, d3] and [d8, d9, d10] corresponds to ID = 1 and, [d5, d6, d7]
    corresponds to ID = 2.
    
    The matrix "se_mat" knows the location of the data for each ID. In this
    function, we specify the "id" for the data we want to extract and we give
    it the "data_vec" and we return the subset of "data_vec" which corresponds
    to te ID we specified. Note that "data" vec needs to be a one-dimensional
    numpy array or Python list, however, the function will return a two-
    dimensional numpy vector. I.e, a vertical numpy vector. This is technically
    2D since to index the data entries we need to indices, such as: [ii,0].

    Args:
        id (int): The ID who's data we will extract from "data_vec".
        data_vec (numpy array): The data_vec we will extract the data from.
            This vector must be a 1D numpy vector (i.e. NOT a vertical vector)
            or a Python list.
        se_mat (numpy array): sesew matrix for data_vec.
        sub_index (int, optional): If there are multiple instances of this ID,
            decide which instance to extract data for. Defaults to None, this
            returns all instances concatenated into a single vector.
        print_error (bool, optional): If ID is not in se_mat, print this error
            to stdout. Defaults to True, set to False if you don't want to
            print this error message.

    Returns:
        numpy data_vec: Subset of "data_vec" corresponding to "id"
    """
    # Check the shape of the input array. First we will check if the input
    # array is 3D. If it is we raise an error.
    try: 
        # Try to index 2D, if this fails then data_vec is 1D (or less)
        data_vec[0,0]
        # If the shape is higher than 1D then we have an error on our hands so
        # break out of the function now and let whoever called the function
        # deal with it.
        print(f"!!! ERROR: In se_extraction expected 1D input for \"data_vec\" but got something higher.")
        error_variable = True
        assert error_variable != True
        return None
    except Exception:
        # If we've reached this point then we've got a 1D input array. We only
        # need one column for the output data_vec since we know we've got a 1D
        # input array.
        num_cols = ONE

    # Initialise the number of IDs and an index variable to store the index of
    # the ID we're interested in if we find it    
    num_ids = len(se_mat[:,0])
    ii = 0

    # Now loop through the sese data_vec looking for the ID we're interested
    # in. If we find this ID then we'll rememebr its index and break out of
    # this loop.
    while ii < num_ids:
        # Check if we've found the ID
        if id == se_mat[ii,0]:
            break
        # Increment index
        ii += 1
        # If ii == num_ids then we couldn't find the ID, print a warning
        # message and return from this function
        if ii == num_ids:
            if print_error:
                print(f"!!! WARNING: ID {str(id)} not found in the sese matrix you provided")
            return None

    # Now that we know what row of the sese data_vec to look at, we'll use the
    # sese data_vec to extract the data we're interested.
    # 
    # Calculate the number of rows in our output data_vec. The following loop
    # is perform twice so that we can learn the size of the output data vector
    # before hand. By doing this we can specify it's size straight away instead
    # of concatenating vectors (which is slower).
    num_rows = 0
    for ii_sub in range(se_mat[ii,1]):
        if sub_index:
            # We want to extract a specific subset of the data corresponding
            # to this ID
            if sub_index == ii_sub:
                num_rows += se_mat[ii, 3 + 2 * ii_sub] + ONE - se_mat[ii, 2 + 2 * ii_sub]
        else:
            # We want all the data for this ID
            num_rows += se_mat[ii, 3 + 2 * ii_sub] + ONE - se_mat[ii, 2 + 2 * ii_sub]
    
    # Initialise a data_vec (with zero rows). As we extract data corresponding to
    # the ID we want we'll concatenate onto this data_vec.
    data_vec_id = np.zeros((num_rows, num_cols))

    # Extract the data
    ii_start = 0
    for ii_sub in range(se_mat[ii,1]):
        if sub_index:
            # We want to extract a specific subset of the data corresponding
            # to this ID
            if sub_index == ii_sub:
                len_of_data = se_mat[ii, 3 + 2 * ii_sub] + ONE - se_mat[ii, 2 + 2 * ii_sub]
                data_vec_id[ii_start:len_of_data, 0] = data_vec[se_mat[ii, 2 + 2 * ii_sub]:se_mat[ii, 3 + 2 * ii_sub] + ONE]

        else:
            # We want all the data for this ID so concatenate the data for each
            # sub index into one data data_vec
            len_of_data = se_mat[ii, 3 + 2 * ii_sub] + ONE - se_mat[ii, 2 + 2 * ii_sub]
            data_vec_id[ii_start:ii_start+len_of_data, 0] = data_vec[se_mat[ii, 2 + 2 * ii_sub]:se_mat[ii, 3 + 2 * ii_sub] + ONE]
            ii_start = len_of_data

    return data_vec_id


def moving_average(y, x=[], n=None):
    """Calculate the moving average of input y with respect to x

    Args:
        y (1D array): Vector to calculate the moving average of
        x (1D array): The horizontal (e.g. time) vector corresponding to y
        n (1D array): The moving average window size

    Returns:
        ma (np row vec): Moving average of y
        ma_x (np row vec): Horizontal axis (e.g. time) vector corresponding to moving
                         average of y
    """
    """Check the optional input arguments"""
    if len(x) == 0:
        x = np.arange(len(y))
    assert n != None

    """Length of our input vector"""
    num_data_points = len(y)

    """Check lengths of input vectors are ok"""
    assert n > 0
    assert type(n) == int
    assert num_data_points - (n-1) > 0
    assert num_data_points == len(x)

    """Vectors for moving average and corresponding time"""
    mov_avg_len = num_data_points - (n-1)
    ma = np.zeros(mov_avg_len)
    ma_x = np.zeros(mov_avg_len)

    """Calculate moving average"""
    ii_start = n - 1
    for ii in range(mov_avg_len):
        """Index that we start reading from in input vector"""
        jj = ii_start + ii

        """Moving avg and corresponding time"""
        ma[ii] = np.mean(y[ii:jj+1]) # "+1" is because of Python indexing convention
        ma_x[ii] = x[jj]

    return ma, ma_x


def get_dict_key_given_value_list_element(dict, value):
    """Get the key of a dictionary given a value. Note that in this case the
    value of the dictionary is a list. So we're looking for a value in a list
    and returning the key of the dictionary that corresponds to that value.

    Args:
        dict (dict): Dictionary to search through
        value (any): Value to search for

    Returns:
        key (any): Key of dictionary that corresponds to the input value
    """
    for key, value_list in dict.items():
        if value in value_list:
            return key
    return None


def normalise_matrix_rows(mat):
    """Normalise the rows of a matrix

    Args:
        mat (np array): Matrix to normalise

    Returns:
        mat_norm (np array): Normalised matrix
    """
    for ii in range(mat.shape[0]):
        row_sum = np.sum(mat[ii,:])
        if row_sum > 0:
            mat[ii,:] = mat[ii,:] / row_sum
    return mat

