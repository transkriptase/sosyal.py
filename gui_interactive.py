import h5py
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from fillmissing import fill_missing
from loadh5 import load_h5_data
from cleaning import clean_and_validate_data
from proximity import detect_proximity_interactions_with_nodes_and_angles
import pickle

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

# Function to preprocess and save interactions
def preprocess_interactions(filename, locations):
    interactions = detect_proximity_interactions_with_nodes_and_angles(locations, proximity_threshold=400, min_angle=50, max_angle=130)
    with open(filename, 'wb') as f:
        pickle.dump(interactions, f)
    return interactions

# GUI function for digital imprinting
class DigitalImprintApp:
    def __init__(self, locations, interactions, x_min, x_max, y_min, y_max, track_names=None, node_names=None):
        self.locations = locations
        self.interactions = interactions
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.track_names = track_names
        self.node_names = node_names
        self.frame = 0
        self.fig, self.ax = plt.subplots()
        self.create_plot()
        self.create_navigation_buttons()
        plt.show()

    def create_plot(self):
        self.ax.clear()
        self.ax.set_title(f"Digital Imprint for Frame {self.frame}")
        self.ax.set_xlabel("X Coordinate (pixels)")
        self.ax.set_ylabel("Y Coordinate (pixels)")

        # Set limits dynamically based on .h5 data
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        frame_count, num_nodes, _, num_termites = self.locations.shape
        colors = plt.cm.get_cmap('tab20', num_termites)  # Colormap to differentiate termites

        # Plot all termite tracks for the selected frame
        for termite in range(num_termites):
            x_coords = [self.locations[self.frame, node, 0, termite] for node in range(num_nodes)]
            y_coords = [self.locations[self.frame, node, 1, termite] for node in range(num_nodes)]
            self.ax.plot(x_coords, y_coords, color=colors(termite), linestyle='-', linewidth=1, alpha=0.5)

        # Flip the y-axis to match the real image orientation
        self.ax.invert_yaxis()

        # Add optimized interaction markers
        interaction_points = set()
        for interaction in self.interactions:
            active, passive, node, start_frame, end_frame = interaction
            if start_frame <= self.frame <= end_frame:
                interaction_x = self.locations[self.frame, node, 0, passive]
                interaction_y = self.locations[self.frame, node, 1, passive]
                interaction_points.add((interaction_x, interaction_y))

        # Plot interaction points as smaller red stars
        if interaction_points:
            interaction_points = np.array(list(interaction_points))
            self.ax.scatter(interaction_points[:, 0], interaction_points[:, 1], c='red', marker='*', s=50, label='Interaction Point')

        self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
        plt.tight_layout()
        self.fig.canvas.draw()

    def create_navigation_buttons(self):
        axprev = plt.axes([0.7, 0.01, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.01, 0.1, 0.075])
        self.bnext = Button(axnext, 'Next >')
        self.bnext.on_clicked(self.next_frame)
        self.bprev = Button(axprev, '< Prev')
        self.bprev.on_clicked(self.prev_frame)

    def next_frame(self, event):
        if self.frame < self.locations.shape[0] - 1:
            self.frame += 1
            self.create_plot()

    def prev_frame(self, event):
        if self.frame > 0:
            self.frame -= 1
            self.create_plot()

# Main code
if __name__ == "__main__":
    # Load data using the load_h5_data function from loadh5.py
    filename = "h5try/7_3_dev.h5"  # Replace with your actual file path
    frame_count, node_count, instance_count, locations, track_names, node_names = load_h5_data(filename)

    # Clean and validate the data using the function from cleaning.py
    cleaned_locations = clean_and_validate_data(locations)

    # Fill missing data (if needed)
    filled_locations = fill_missing(cleaned_locations)

    # Preprocess and load interactions
    interactions_file = "interactions.pkl"
    try:
        with open(interactions_file, 'rb') as f:
            interactions = pickle.load(f)
    except FileNotFoundError:
        interactions = preprocess_interactions(interactions_file, filled_locations)

    print("Detected Interactions with Node and Angle Information:")
    for interaction in interactions:
        print(f"Active termite {interaction[0]} interacted with passive termite {interaction[1]} at node {interaction[2]} between frames {interaction[3]} and {interaction[4]}")

    # Get x and y range from the .h5 file
    x_min, x_max, y_min, y_max = get_xy_range(filename)

    # Create GUI for visualizing specific frames
    DigitalImprintApp(filled_locations, interactions, x_min, x_max, y_min, y_max, track_names=track_names, node_names=node_names)
