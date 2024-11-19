import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def calculate_distance(point1, point2):
    """Calculate the Euclidean distance between two points in pixels."""
    return np.linalg.norm(point1 - point2)

def calculate_angle(point1, point2):
    """Calculate the angle between two points relative to the horizontal axis."""
    vector = point2 - point1
    angle = np.degrees(np.arctan2(vector[1], vector[0]))  # Angle in degrees
    return angle if angle >= 0 else angle + 360  # Normalize to [0, 360]

def is_within_angle_range(angle, min_angle=50, max_angle=130):
    """Check if the angle is within the defined range."""
    return min_angle <= angle <= max_angle

def detect_proximity_interactions_with_nodes_and_angles(locations, proximity_threshold=400, min_angle=50, max_angle=130, min_duration_frames=60):
    """Detect interactions where the active termite's mandible interacts with any of the passive termite's nodes, considering distance and angle."""
    frame_count, num_nodes, _, num_termites = locations.shape
    interactions = []
    
    mandible_index = 0

    for active in range(num_termites):
        for passive in range(num_termites):
            if active == passive:
                continue

            start_frame = None
            duration = 0
            interacting_node = None

            for frame in range(frame_count):
                active_mandible_location = locations[frame, mandible_index, :, active]

                for node in range(num_nodes):
                    passive_node_location = locations[frame, node, :, passive]
                    distance = calculate_distance(active_mandible_location, passive_node_location)
                    angle = calculate_angle(active_mandible_location, passive_node_location)

                    if distance < proximity_threshold and is_within_angle_range(angle, min_angle, max_angle):
                        if start_frame is None:
                            start_frame = frame
                        duration += 1
                        interacting_node = node
                        break  
                    else:
                        if duration >= min_duration_frames:
                            interactions.append((active, passive, interacting_node, start_frame, frame - 1))
                        start_frame = None
                        duration = 0
                        interacting_node = None

                if duration >= min_duration_frames and interacting_node is not None:
                    interactions.append((active, passive, interacting_node, start_frame, frame - 1))

    return interactions

"""

def animate_interactions(locations, interactions):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1000)  # Adjust based on your coordinate range
    ax.set_ylim(0, 1000)
    
    num_termites = locations.shape[3]
    scatter_plots = [ax.scatter([], [], label=f"Termite {i}") for i in range(num_termites)]
    
    def update(frame):
        ax.clear()
        ax.set_title(f"Termite Interactions at Frame {frame}")
        ax.set_xlim(0, 1000)
        ax.set_ylim(0, 1000)
        
        for i in range(num_termites):
            x, y = locations[frame, 0, :, i], locations[frame, 1, :, i]
            scatter_plots[i] = ax.scatter(x, y, label=f"Termite {i}")
        
        for interaction in interactions:
            active, passive, node, start_frame, end_frame = interaction
            if start_frame <= frame <= end_frame:
                active_x, active_y = locations[frame, 0, :, active], locations[frame, 1, :, active]
                passive_x, passive_y = locations[frame, 0, :, passive], locations[frame, 1, :, passive]
                ax.plot([active_x, passive_x], [active_y, passive_y], 'r-', linewidth=2)
                ax.scatter(passive_x[node], passive_y[node], color='r', s=100, label=f'Node {node}')

    anim = FuncAnimation(fig, update, frames=locations.shape[0], interval=100)
    plt.show()

"""
