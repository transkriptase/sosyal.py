import h5py
import numpy as np
from fillmissing import fill_missing
from cleaning import clean_and_validate_data

#filename = "C+1_1_0.h5"
#filename = "7.h5"

def load_h5_data(filename):
    with h5py.File(filename, "r") as f:
        track_names = [n.decode() for n in f["track_names"][:]]
        locations = f["tracks"][:].T
        frame_count, node_count, _, instance_count = locations.shape
        node_names = [n.decode() for n in f["node_names"][:]]
        
        #print("Dataset names:", list(f.keys()))
        #print("\n===== TRACK NAMES =====")
        #print(track_names)
        #f.visititems(print_attributes)
    
    #print(frame_count)
    #print(instance_count)
    return frame_count, node_count, instance_count, locations, track_names, node_names
"""
def print_attributes(name, obj):
    print(name)
    for key, val in obj.attrs.items():
        print("  {}: {}".format(key, val))
    print("  Type: {}".format(type(obj)))
    if isinstance(obj, h5py.Dataset):
        print("  Shape: {}".format(obj.shape))
        print("  Data Type (dtype): {}".format(obj.dtype))
    print("==================================")
"""

def print_attributes(name, obj):
    print(name)
    for key, val in obj.attrs.items():
        print("  {}: {}".format(key, val))
    print("  Type: {}".format(type(obj)))
    if isinstance(obj, h5py.Dataset):
        print("  Shape: {}".format(obj.shape))
        print("  Data Type (dtype): {}".format(obj.dtype))
    print("==================================")

import numpy as np
from fillmissing import fill_missing
from cleaning import clean_and_validate_data

def analyze_proximity(locations, proximity_threshold=100):
    """Analyze and detect proximity interactions between termites."""
    frame_count, _, _, num_termites = locations.shape
    interaction_counts = np.zeros((num_termites, num_termites))

    for frame in range(frame_count):
        for i in range(num_termites):
            for j in range(i + 1, num_termites):
                distance = np.linalg.norm(locations[frame, 1, :, i] - locations[frame, 1, :, j])
                if distance < proximity_threshold:
                    interaction_counts[i, j] += 1
                    interaction_counts[j, i] += 1  # Symmetric relationship
    
    return interaction_counts

def summarize_interactions(interaction_counts, frame_count):
    """Summarize the interactions as a percentage of total frames."""
    num_termites = interaction_counts.shape[0]
    interaction_summary = {}
    
    for i in range(num_termites):
        partners = {
            j: (interaction_counts[i, j] / frame_count) * 100 
            for j in range(num_termites) if i != j and interaction_counts[i, j] > 0
        }
        interaction_summary[f"Termite {i}"] = partners

    return interaction_summary

# Sample code to run the analysis
filename = "h5try/7_3_dev.h5"
frame_count, node_count, instance_count, locations, track_names, node_names = load_h5_data(filename)
filled_locations = fill_missing(locations)

# Analyze interactions
interaction_counts = analyze_proximity(filled_locations)
interaction_summary = summarize_interactions(interaction_counts, frame_count)

# Print the interaction summary
for termite, interactions in interaction_summary.items():
    print(f"{termite} interactions:")
    for partner, percentage in interactions.items():
        print(f"  With {partner}: {percentage:.2f}% of frames")
    print()
