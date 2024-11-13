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

def calculate_angle(location1, location2):
    """Calculate the angle between two points (location1, location2)."""
    vector = location2 - location1
    angle = np.degrees(np.arctan2(vector[1], vector[0]))  # Calculate the angle in degrees
    return angle if angle >= 0 else angle + 360  # Normalize angle to [0, 360]

def is_within_angle(angle, min_angle=90, max_angle=130):
    """Check if the angle is within the specified range."""
    return min_angle <= angle <= max_angle

def analyze_proximity_with_distance_and_time(locations, proximity_threshold=100, min_angle=90, max_angle=130, min_duration_frames=60):
    """Analyze and detect proximity interactions between termites with antenna reach, angle, and duration filters."""
    frame_count, _, _, num_termites = locations.shape
    interactions = []

    for i in range(num_termites):
        for j in range(i + 1, num_termites):
            start_frame = None
            duration = 0

            for frame in range(frame_count):
                distance = np.linalg.norm(locations[frame, 1, :, i] - locations[frame, 1, :, j])
                if distance < proximity_threshold:
                    angle = calculate_angle(locations[frame, 1, :, i], locations[frame, 1, :, j])
                    if is_within_angle(angle, min_angle, max_angle):
                        if start_frame is None:
                            start_frame = frame
                        duration += 1
                    else:
                        if duration >= min_duration_frames:
                            interactions.append((i, j, start_frame, frame - 1))
                        start_frame = None
                        duration = 0
                else:
                    if duration >= min_duration_frames:
                        interactions.append((i, j, start_frame, frame - 1))
                    start_frame = None
                    duration = 0

            if duration >= min_duration_frames:
                interactions.append((i, j, start_frame, frame_count - 1))

    return interactions

# Sample code to run the analysis
filename = "h5try/7_3_dev.h5"
frame_count, node_count, instance_count, locations, track_names, node_names = load_h5_data(filename)
filled_locations = fill_missing(locations)

# Analyze interactions considering distance, angle, and time
interactions = analyze_proximity_with_distance_and_time(filled_locations)

# Print the interactions
print("Detected Interactions (with distance and time filters):")
for interaction in interactions:
    print(f"Termites {interaction[0]} and {interaction[1]} interacted between frames {interaction[2]} and {interaction[3]}")
