import h5py
import numpy as np
from fillmissing import fill_missing
from cleaning import clean_and_validate_data

def load_h5_data(filename):
    with h5py.File(filename, "r") as f:
        track_names = [n.decode() for n in f["track_names"][:]]
        locations = f["tracks"][:].T
        frame_count, node_count, _, instance_count = locations.shape
        node_names = [n.decode() for n in f["node_names"][:]]
        
    return frame_count, node_count, instance_count, locations, track_names, node_names

def print_attributes(name, obj):
    print(name)
    for key, val in obj.attrs.items():
        print("  {}: {}".format(key, val))
    print("  Type: {}".format(type(obj)))
    if isinstance(obj, h5py.Dataset):
        print("  Shape: {}".format(obj.shape))
        print("  Data Type (dtype): {}".format(obj.dtype))
    print("==================================")

# Function to analyze proximity interactions
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

# Function to detect mutual grooming interactions
def detect_mutual_grooming(locations, distance_threshold=500, min_duration_frames=60):
    """Detect mutual grooming interactions between pairs of termites."""
    frame_count, _, _, num_termites = locations.shape
    grooming_events = []

    for i in range(num_termites):
        for j in range(i + 1, num_termites):
            start_frame = None
            duration = 0

            for frame in range(frame_count):
                distance = np.linalg.norm(locations[frame, 1, :, i] - locations[frame, 1, :, j])

                if distance <= distance_threshold:
                    if start_frame is None:
                        start_frame = frame
                    duration += 1
                else:
                    if duration >= min_duration_frames:
                        grooming_events.append((i, j, start_frame, frame - 1))
                    start_frame = None
                    duration = 0

            if duration >= min_duration_frames:
                grooming_events.append((i, j, start_frame, frame_count - 1))

    return grooming_events

# Function to detect self-grooming behavior
def detect_self_grooming(locations, min_movement=10, min_duration_frames=60):
    """Identify self-grooming behavior based on specific body part movement."""
    frame_count, _, _, num_termites = locations.shape
    self_grooming_events = []

    for termite_idx in range(num_termites):
        start_frame = None
        duration = 0

        for frame in range(1, frame_count):
            body_part_movement = np.linalg.norm(locations[frame, 1, :, termite_idx] - locations[frame - 1, 1, :, termite_idx])
            
            if body_part_movement > min_movement:
                if start_frame is None:
                    start_frame = frame
                duration += 1
            else:
                if duration >= min_duration_frames:
                    self_grooming_events.append((termite_idx, start_frame, frame - 1))
                start_frame = None
                duration = 0

        if duration >= min_duration_frames:
            self_grooming_events.append((termite_idx, start_frame, frame_count - 1))

    return self_grooming_events

# Sample code to run the analysis
filename = "h5try/7_3_dev.h5"
frame_count, node_count, instance_count, locations, track_names, node_names = load_h5_data(filename)
filled_locations = fill_missing(locations)

# Analyze interactions
interaction_counts = analyze_proximity(filled_locations)
interaction_summary = summarize_interactions(interaction_counts, frame_count)

# Detect mutual grooming and self-grooming events
mutual_grooming_events = detect_mutual_grooming(filled_locations)
self_grooming_events = detect_self_grooming(filled_locations)

# Print the interaction summary
#for termite, interactions in interaction_summary.items():
    #print(f"{termite} interactions:")
    #for partner, percentage in interactions.items():
        #print(f"  With {partner}: {percentage:.2f}% of frames")
    #print()

# Print mutual grooming events
print("Mutual Grooming Events:")
for event in mutual_grooming_events:
    print(f"Termites {event[0]} and {event[1]} groomed between frames {event[2]} and {event[3]}")

# Print self-grooming events
print("\nSelf-Grooming Events:")
for event in self_grooming_events:
    print(f"Termite {event[0]} performed self-grooming between frames {event[1]} and {event[2]}")
