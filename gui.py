import h5py
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from fillmissing import fill_missing
from loadh5 import load_h5_data
from cleaning import clean_and_validate_data
from proximity import detect_proximity_interactions_with_nodes_and_angles

# Function to calculate x and y range from .h5 file
def get_xy_range(filename):
    with h5py.File(filename, "r") as f:
        locations = f["tracks"][:]
        x_coords = locations[:, :, 0, :].flatten()
        y_coords = locations[:, :, 1, :].flatten()

        # Filter out NaN values
        x_coords_clean = x_coords[~np.isnan(x_coords)]
        y_coords_clean = y_coords[~np.isnan(y_coords)]

        x_min, x_max = x_coords_clean.min(), x_coords_clean.max()
        y_min, y_max = y_coords_clean.min(), y_coords_clean.max()

    return x_min, x_max, y_min, y_max

# GUI function for digital imprinting
def digital_imprint_frame(locations, frame, interactions, x_min, x_max, y_min, y_max, track_names=None, node_names=None):
    """Create a digital imprint for a specific frame."""
    if frame >= locations.shape[0]:
        messagebox.showerror("Invalid Frame", f"Frame {frame} is out of range. Maximum frame number is {locations.shape[0] - 1}.")
        return

    fig, ax = plt.subplots()
    ax.set_title(f"Digital Imprint for Frame {frame}")
    ax.set_xlabel("X Coordinate (pixels)")
    ax.set_ylabel("Y Coordinate (pixels)")

    # Set limits dynamically based on .h5 data
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    frame_count, num_nodes, _, num_termites = locations.shape
    colors = plt.cm.get_cmap('tab20', num_termites)  # Colormap to differentiate termites

    # Plot all termite tracks
    for termite in range(num_termites):
        x_coords = [locations[frame, node, 0, termite] for node in range(num_nodes)]
        y_coords = [locations[frame, node, 1, termite] for node in range(num_nodes)]
        ax.plot(x_coords, y_coords, color=colors(termite), alpha=0.6, label=f'Termite {termite}' if track_names is None else f'{track_names[termite]}')

    # Connect dots to show whole termite individuals
    for termite in range(num_termites):
        x_coords = [locations[frame, node, 0, termite] for node in range(num_nodes)]
        y_coords = [locations[frame, node, 1, termite] for node in range(num_nodes)]
        ax.plot(x_coords, y_coords, color=colors(termite), linestyle='-', linewidth=1, alpha=0.5)

    # Flip the y-axis to match the real image orientation
    ax.invert_yaxis()

    # Add optimized interaction markers
    interaction_points = set()
    for interaction in interactions:
        active, passive, node, start_frame, end_frame = interaction
        if start_frame <= frame <= end_frame:
            interaction_x = locations[frame, node, 0, passive]
            interaction_y = locations[frame, node, 1, passive]
            interaction_points.add((interaction_x, interaction_y))

    # Plot interaction points as smaller red stars
    if interaction_points:
        interaction_points = np.array(list(interaction_points))
        ax.scatter(interaction_points[:, 0], interaction_points[:, 1], c='red', marker='*', s=50, label='Interaction Point')

    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    plt.tight_layout()
    plt.show()

# GUI for Frame Selection
def create_gui(locations, interactions, x_min, x_max, y_min, y_max, track_names=None, node_names=None):
    root = tk.Tk()
    root.withdraw()  # Hide the root window as we only need the dialog

    while True:
        try:
            frame = simpledialog.askinteger("Input", "Enter frame number to visualize (or Cancel to exit):", minvalue=0)
            if frame is None:
                break  # User clicked cancel

            digital_imprint_frame(locations, frame=frame, interactions=interactions, 
                                 x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, 
                                 track_names=track_names, node_names=node_names)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Main code
if __name__ == "__main__":
    # Load data using the load_h5_data function from loadh5.py
    filename = "h5try/7_3_dev.h5"  # Replace with your actual file path
    frame_count, node_count, instance_count, locations, track_names, node_names = load_h5_data(filename)

    # Clean and validate the data using the function from cleaning.py
    cleaned_locations = clean_and_validate_data(locations)

    # Fill missing data (if needed)
    filled_locations = fill_missing(cleaned_locations)

    # Detect and print proximity interactions with nodes and angles
    interactions = detect_proximity_interactions_with_nodes_and_angles(filled_locations, proximity_threshold=400, min_angle=50, max_angle=130)
    print("Detected Interactions with Node and Angle Information:")
    for interaction in interactions:
        print(f"Active termite {interaction[0]} interacted with passive termite {interaction[1]} at node {interaction[2]} between frames {interaction[3]} and {interaction[4]}")

    # Get x and y range from the .h5 file
    x_min, x_max, y_min, y_max = get_xy_range(filename)

    # Create GUI for visualizing specific frames
    create_gui(filled_locations, interactions, x_min, x_max, y_min, y_max, track_names=track_names, node_names=node_names)
