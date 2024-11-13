# beskasim.py
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fillmissing import fill_missing
from cleaning import clean_and_validate_data
from loadh5 import load_h5_data
from connect_broken_tracks import (connect_broken_tracks, calculate_distance, 
                                   find_start_end_frames, generate_connected_track_name, 
                                   circle_check, create_new_tracks, complete_new_tracks)
from groom import detect_grooming_events

# Directory paths
directory = "h5try"
output_directory = "output_try"

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)


def calculate_angle(vector1, vector2):
    """Calculate the angle (in degrees) between two vectors."""
    unit_vector1 = vector1 / np.linalg.norm(vector1)
    unit_vector2 = vector2 / np.linalg.norm(vector2)
    dot_product = np.dot(unit_vector1, unit_vector2)
    angle = np.arccos(np.clip(dot_product, -1.0, 1.0))
    return np.degrees(angle)

def save_distances_to_file(distances, output_filename):
    """Save distances to a file."""
    with open(output_filename, 'w') as f:
        for track_name, distance in distances.items():
            f.write(f"{track_name}: {distance}\n")

def save_individuals_count_to_file(individuals_count, output_directory):
    """Save the number of individuals detected in the first frame."""
    output_path = os.path.join(output_directory, "number_of_individuals.txt")
    with open(output_path, 'w') as f:
        for filename, count in individuals_count.items():
            f.write(f"{filename}: {count}\n")

def plot_tracks(locations, track_names, filename):
    """Plot tracks for each individual and save as an image."""
    plt.figure(figsize=(10, 8))
    for track_idx in range(locations.shape[3]):
        track_data = locations[:, :, :, track_idx]
        x_data, y_data = track_data[:, 0, 0], track_data[:, 0, 1]
        valid_indices = ~np.isnan(x_data) & ~np.isnan(y_data)
        
        if valid_indices.any():
            plt.plot(x_data[valid_indices], y_data[valid_indices])
            
    plt.title(f"Tracks for {filename}")
    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    output_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_results.png")
    plt.savefig(output_path)
    plt.close()

def plot_distance_scatter(distances, filename):
    """Plot a scatter plot for total distance traveled by each track."""
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=list(distances.keys()), y=list(distances.values()), s=100)
    plt.xlabel("Tracks")
    plt.ylabel("Total Distance")
    plt.xticks(rotation=90)
    plt.title(f"Total Distance Traveled by Each Track in {filename}")
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    output_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_distances.png")
    plt.savefig(output_path)
    plt.close()

def process_file(filepath, output_directory):
    """Process individual .h5 file to extract and analyze track data."""
    try:
        # Load file data
        with h5py.File(filepath, "r") as f:
            track_names = [n.decode() for n in f["track_names"][:]]
            locations = f["tracks"][:].T

        # Load and clean data
        frame_count, node_count, instance_count, locations, track_names, node_names = load_h5_data(filepath)
        filled_locations = fill_missing(locations)
        cleaned_dataset = clean_and_validate_data(filled_locations)

        # Detect mandible_abdomen_grooming events
        mandible_abdomen_grooming_events = detect_mandible_abdomen_grooming(
            filled_locations, min_distance=1, max_distance=50, min_duration_frames=45
        )
        
        # Print detected grooming events for verification
        print("Detected mandible_abdomen_grooming events:")
        for event in mandible_abdomen_grooming_events:
            termite_a, termite_b, start_frame, end_frame = event
            print(f"  - Grooming between tracks {termite_a} and {termite_b} from frame {start_frame} to {end_frame}")

        # Connect broken tracks and calculate distances
        track_start_end_frames = {
            track_names[track_idx]: find_start_end_frames(track_idx, locations)
            for track_idx in range(locations.shape[3])
        }
        
        # Separate broken and complete tracks
        tracks_starting_at_zero = {k: v for k, v in track_start_end_frames.items() if v[0] == 0}
        not_real_tracks = {k: v for k, v in track_start_end_frames.items() if k not in tracks_starting_at_zero}
        not_broken_tracks = {k: v for k, v in tracks_starting_at_zero.items() if v[1] == frame_count - 1}
        broken_tracks = {k: v for k, v in tracks_starting_at_zero.items() if v[1] != frame_count - 1}

        # Connect broken tracks
        connected_tracks, completed_tracks, track_chains = connect_broken_tracks(
            broken_tracks, not_real_tracks, frame_threshold=100, distance_threshold=2000,
            radius=90, filled_locations=filled_locations, track_names=track_names, frame_count=frame_count
        )
        
        # Calculate distances for complete tracks
        distances = {}
        for track_name in not_broken_tracks:
            track_idx = track_names.index(track_name)
            track_points = locations[:, :, :, track_idx]
            # Assuming point1 and point2 should be consecutive frames for distance calculation
            distances[track_name] = np.nansum([
                calculate_distance(track_points[frame, :, :], track_points[frame + 1, :, :])
                for frame in range(frame_count - 1)
                if not np.isnan(track_points[frame, :, :]).any() and not np.isnan(track_points[frame + 1, :, :]).any()
            ])
        
        # Calculate distances for connected tracks
        for new_track_name, track_chain in track_chains.items():
            x_data = np.concatenate([filled_locations[:, 0, 0, track_names.index(tn)] for tn in track_chain])
            y_data = np.concatenate([filled_locations[:, 0, 1, track_names.index(tn)] for tn in track_chain])
            distances[new_track_name] = np.nansum(np.sqrt(np.diff(x_data) ** 2 + np.diff(y_data) ** 2))

        # Save results
        save_distances_to_file(distances, os.path.join(output_directory, f"{os.path.splitext(filepath)[0]}_distances.txt"))
        plot_tracks(filled_locations, track_names, os.path.basename(filepath))
        plot_distance_scatter(distances, os.path.basename(filepath))

    except Exception as e:
        print(f"Error processing '{filepath}': {e}")



if __name__ == "__main__":
    # .h5 dosyasını yükle
    filepath = "h5try/7_3_dev.h5"  # Dosya yolunu kendi dosyanızla değiştirin
    frame_count, node_count, instance_count, locations, track_names, node_names = load_h5_data(filepath)
    
    # Grooming olaylarını tespit et
    grooming_events = detect_grooming_events(locations, min_distance=1, max_distance=50, min_duration_frames=45)
    
    # Tespit edilen grooming olaylarını yazdır
    print("Detected grooming events:")
    for event in grooming_events:
        track_a, track_b, start_frame, end_frame = event
        print(f"Grooming between tracks {track_a} and {track_b} from frame {start_frame} to {end_frame}")
    
    # Grooming olaylarını görselleştir
    plot_grooming_timeline(grooming_events)