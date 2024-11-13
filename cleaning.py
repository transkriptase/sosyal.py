import numpy as np

def clean_and_validate_data(dataset):
    """
    Cleans and validates the termite dataset.

    Parameters:
    - dataset (numpy.array): The multi-dimensional array containing the termite data with X and Y coordinates.

    Returns:
    - numpy.array: Cleaned and validated dataset.
    """

    # 1. Ensure there are no missing values
    if np.isnan(dataset).any():
        print("Warning: Missing values detected!")
        # Display the count of missing values
        missing_values_count = np.isnan(dataset).sum()
        print(f"There are {missing_values_count} missing values.")
        # Implement your strategy to handle the NaNs here.

    # 2. Validate the scale and range of the X and Y coordinates
    X_MIN, X_MAX = 0, 1000
    Y_MIN, Y_MAX = 0, 1000

    invalid_x_coords = (dataset[:, 0, :, :] < X_MIN) | (dataset[:, 0, :, :] > X_MAX)
    invalid_y_coords = (dataset[:, 1, :, :] < Y_MIN) | (dataset[:, 1, :, :] > Y_MAX)
    
    if invalid_x_coords.any():
        print("Warning: Some X coordinates are out of the expected range!")
        # Display the count of invalid X coordinates
        invalid_x_count = invalid_x_coords.sum()
        print(f"There are {invalid_x_count} invalid X coordinates.")
        
    if invalid_y_coords.any():
        print("Warning: Some Y coordinates are out of the expected range!")
        # Display the count of invalid Y coordinates
        invalid_y_count = invalid_y_coords.sum()
        print(f"There are {invalid_y_count} invalid Y coordinates.")
    
    # Implement your strategy to handle the invalid coordinates here.

    return dataset
