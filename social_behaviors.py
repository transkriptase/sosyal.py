
import numpy as np

def calculate_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return np.linalg.norm(point1 - point2)

def detect_proximity_interactions(locations, proximity_threshold=100, min_duration_frames=60):
    """Detect interactions where termites remain within a certain distance for a given duration.
    
    Parameters:
    - locations (numpy.array): The 4D array with shape (frames, body_parts, coordinates, termites).
    - proximity_threshold (float): The distance threshold for defining proximity.
    - min_duration_frames (int): The minimum number of frames to consider a sustained interaction.

    Returns:
    - list: A list of tuples representing interactions (termite_1, termite_2, start_frame, end_frame).
    """
    frame_count, _, _, num_termites = locations.shape
    interactions = []

    for i in range(num_termites):
        for j in range(i + 1, num_termites):
            start_frame = None
            duration = 0

            for frame in range(frame_count):
                distance = calculate_distance(locations[frame, 1, :, i], locations[frame, 1, :, j])
                if distance < proximity_threshold:
                    if start_frame is None:
                        start_frame = frame
                    duration += 1
                else:
                    if duration >= min_duration_frames:
                        interactions.append((i, j, start_frame, frame - 1))
                    start_frame = None
                    duration = 0

            # Check for interaction that lasts until the last frame
            if duration >= min_duration_frames:
                interactions.append((i, j, start_frame, frame_count - 1))

    return interactions


def calculate_direction_vector(location1, location2):
    """Calculate the direction vector between two consecutive locations."""
    return location2 - location1

def detect_leader_follower_behavior(locations, proximity_threshold=200, min_leader_frames=60):
    """Detect leader-follower behavior between termites.
    
    Parameters:
    - locations (numpy.array): The 4D array with shape (frames, body_parts, coordinates, termites).
    - proximity_threshold (float): The distance threshold for defining proximity.
    - min_leader_frames (int): The minimum number of frames to confirm leader-follower behavior.
    
    Returns:
    - list: A list of tuples representing leader-follower interactions (leader, follower, start_frame, end_frame).
    """
    frame_count, _, _, num_termites = locations.shape
    interactions = []

    for i in range(num_termites):
        for j in range(num_termites):
            if i == j:
                continue

            start_frame = None
            duration = 0

            for frame in range(1, frame_count):  # Start from frame 1 to calculate direction from frame 0
                leader_vector = calculate_direction_vector(locations[frame - 1, 1, :, i], locations[frame, 1, :, i])
                follower_vector = calculate_direction_vector(locations[frame - 1, 1, :, j], locations[frame, 1, :, j])

                # Check if the distance is within proximity threshold
                distance = np.linalg.norm(locations[frame, 1, :, i] - locations[frame, 1, :, j])
                if distance < proximity_threshold:
                    # Check if the leader is moving ahead (dot product positive indicates same direction)
                    dot_product = np.dot(leader_vector, follower_vector)
                    if dot_product > 0:  # Indicates that follower is moving in the same direction
                        if start_frame is None:
                            start_frame = frame
                        duration += 1
                    else:
                        if duration >= min_leader_frames:
                            interactions.append((i, j, start_frame, frame - 1))
                        start_frame = None
                        duration = 0
                else:
                    if duration >= min_leader_frames:
                        interactions.append((i, j, start_frame, frame - 1))
                    start_frame = None
                    duration = 0

            # Check if the behavior lasts until the last frame
            if duration >= min_leader_frames:
                interactions.append((i, j, start_frame, frame_count - 1))

    return interactions
