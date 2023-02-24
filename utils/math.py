import numpy as np

# Takes a numpy array and normalizes the ranges to be between 0 to new_max_value
def normalize(matrix: np.array, new_max_value: int):
    curr_max_value = np.max(matrix)

    normalized_matrix = (matrix/curr_max_value)*new_max_value
    return np.round(normalized_matrix, decimals=1)
