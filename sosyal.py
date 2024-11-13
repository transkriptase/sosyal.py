import h5py
import numpy as np
from loadh5 import load_h5_data
from fillmissing import fill_missing
from social_behaviors import detect_proximity_interactions


filename = "h5try/7_3_dev.h5"
frame_count, node_count, instance_count, locations, track_names, node_names = load_h5_data(filename)
filled_locations = fill_missing(locations)

# Detect and print proximity interactions
interactions = detect_proximity_interactions(filled_locations)
print("Detected Interactions:")
for termite_1, termite_2, start_frame, end_frame in interactions:
    #print(f"Termites {termite_1} and {termite_2} interacted between frames {start_frame} and {end_frame}")


# Detect and print leader-follower behavior
leader_follower_interactions = detect_leader_follower_behavior(filled_locations)
print("\nDetected Leader-Follower Interactions:")
for leader, follower, start_frame, end_frame in leader_follower_interactions:
    print(f"Termite {leader} led termite {follower} from frame {start_frame} to {end_frame}")
