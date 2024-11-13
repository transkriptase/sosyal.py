import numpy as np

def calculate_direction_vector(location1, location2):
    """Calculate the direction vector between two consecutive locations."""
    return location2 - location1

def is_moving(location1, location2, movement_threshold=1.0):
    """Check if a termite is moving by calculating the distance between two consecutive positions."""
    return np.linalg.norm(location2 - location1) > movement_threshold

def detect_leader_follower_behavior(locations, proximity_threshold=1000, min_leader_frames=10, movement_threshold=1.0):
    """Detect leader-follower behavior between termites.
    
    Parameters:
    - locations (numpy.array): The 4D array with shape (frames, body_parts, coordinates, termites).
    - proximity_threshold (float): The distance threshold for defining proximity.
    - min_leader_frames (int): The minimum number of frames to confirm leader-follower behavior.
    - movement_threshold (float): The minimum distance moved between frames to be considered moving.
    
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
                if not (is_moving(locations[frame - 1, 1, :, i], locations[frame, 1, :, i], movement_threshold) and
                        is_moving(locations[frame - 1, 1, :, j], locations[frame, 1, :, j], movement_threshold)):
                    # Skip this frame if either termite is not moving
                    if duration >= min_leader_frames:
                        interactions.append((i, j, start_frame, frame - 1))
                    start_frame = None
                    duration = 0
                    continue

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
