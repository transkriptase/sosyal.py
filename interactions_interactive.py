import numpy as np
import matplotlib.pyplot as plt

def calculate_vector(point1, point2):
    """Calculate the vector from point1 to point2."""
    return point2 - point1

def calculate_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return np.linalg.norm(point2 - point1)

def calculate_angle_between_vectors(vector1, vector2):
    """Calculate the angle between two vectors using the dot product formula."""
    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)
    cosine_angle = dot_product / (magnitude1 * magnitude2)
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))  # Ensuring cosine value is within valid range
    return angle

def is_within_angle_range(angle, min_angle, max_angle):
    """Check if the angle is within a specified range."""
    return min_angle <= angle <= max_angle

def detect_proximity_interactions_with_correct_angles(locations, proximity_threshold=400, min_angle=50, max_angle=130, min_duration_frames=45):
    """Detect interactions considering corrected vector calculations between active and passive termites."""
    frame_count, num_nodes, _, num_termites = locations.shape
    interactions = []
    
    mandible_index = 0
    thorax_index = 1
    abdomen_index = 2

    for active in range(num_termites):
        for passive in range(num_termites):
            if active == passive:
                continue

            start_frame = None
            duration = 0
            interacting_node = None

            for frame in range(frame_count):
                active_mandible_location = locations[frame, mandible_index, :, active]
                active_thorax_location = locations[frame, thorax_index, :, active]
                active_abdomen_location = locations[frame, abdomen_index, :, active]
                
                # Calculate the active termite's vector: mandible -> thorax
                active_vector = calculate_vector(active_mandible_location, active_thorax_location)

                for node in range(num_nodes):
                    passive_node_location_1 = locations[frame, node, :, passive]
                    passive_node_location_2 = locations[frame, (node + 1) % num_nodes, :, passive]  # Ensure connection between nodes
                    
                    # Calculate the passive termite's vector between nodes
                    passive_vector = calculate_vector(passive_node_location_1, passive_node_location_2)

                    # Dynamic proximity threshold based on active termite size (using thorax to abdomen distance as a reference)
                    dynamic_proximity_threshold = min(proximity_threshold, calculate_distance(active_thorax_location, active_mandible_location) * 2.0)

                    distance = calculate_distance(active_mandible_location, passive_node_location_1)
                    angle = calculate_angle_between_vectors(active_vector, passive_vector)

                    # Interaction only possible if angle is greater than 50 degrees and termites are not parallel
                    if distance < dynamic_proximity_threshold and angle > 50:
                        if start_frame is None:
                            start_frame = frame
                        duration += 1
                        interacting_node = node
                    else:
                        # End interaction if conditions are not met and add if valid
                        if duration >= min_duration_frames:
                            interactions.append((active, passive, interacting_node, start_frame, frame - 1))
                        start_frame = None
                        duration = 0
                        interacting_node = None

            # Add remaining interaction if it lasts long enough
            if duration >= min_duration_frames and interacting_node is not None:
                interactions.append((active, passive, interacting_node, start_frame, frame - 1))

    # Print the number of detected interactions
    print(f"Number of interactions detected: {len(interactions)}")
    return interactions
