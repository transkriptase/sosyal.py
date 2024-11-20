
import numpy as np
from fillmissing import fill_missing
from loadh5 import load_h5_data
from cleaning import clean_and_validate_data
from interactions import detect_proximity_interactions_with_correct_angles
from gui import DigitalImprintApp, get_xy_range

# Load data using the load_h5_data function from loadh5.py
filename = "h5try/7_3_dev.h5"  # Replace with your actual file path
"""
try:
    # Load and preprocess data
    print("Loading data...")
    frame_count, node_count, instance_count, locations, track_names, node_names = load_h5_data(filename)
    cleaned_locations = clean_and_validate_data(locations)
    filled_locations = fill_missing(cleaned_locations)

    # Detect and print proximity interactions with nodes and angles
    interactions = detect_proximity_interactions_with_nodes_and_angles(
        filled_locations,
        proximity_threshold=400,
        min_angle=50,
        max_angle=130
    )
    print("Detected Interactions with Node and Angle Information:")
    for interaction in interactions:
        print(f"Active termite {interaction[0]} interacted with passive termite {interaction[1]} at node {interaction[2]} "
              f"between frames {interaction[3]} and {interaction[4]}")

    # Launch the GUI for interactive visualization
    create_gui(filled_locations, interactions, track_names=track_names, node_names=node_names)

except Exception as e:
    print(f"An error occurred: {e}")
"""

if __name__ == "__main__":
    # Load data using the load_h5_data function from loadh5.py
    filename = "h5try/7_3_dev.h5"  # Replace with your actual file path
    frame_count, node_count, instance_count, locations, track_names, node_names = load_h5_data(filename)

    # Clean and validate the data using the function from cleaning.py
    cleaned_locations = clean_and_validate_data(locations)

    # Fill missing data (if needed)
    filled_locations = fill_missing(cleaned_locations)

    # Detect and print proximity interactions with nodes and angles
    #interactions = detect_proximity_interactions_with_nodes_and_angles(filled_locations, proximity_threshold=400, min_angle=50, max_angle=130)
    interactions = detect_proximity_interactions_with_correct_angles(filled_locations, proximity_threshold=400, min_angle=50, max_angle=130)
    print("Detected Interactions with Node and Angle Information:")
    for interaction in interactions:
        print(f"Active termite {interaction[0]} interacted with passive termite {interaction[1]} at node {interaction[2]} between frames {interaction[3]} and {interaction[4]}")

    # Get x and y range from the .h5 file
    x_min, x_max, y_min, y_max = get_xy_range(filename)

    # Create GUI for visualizing specific frames
    DigitalImprintApp(filled_locations, interactions, x_min, x_max, y_min, y_max, track_names=track_names, node_names=node_names)
