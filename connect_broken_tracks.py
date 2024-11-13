import h5py
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from fillmissing import fill_missing
from cleaning import clean_and_validate_data
from loadh5 import load_h5_data


def calculate_distance(point1, point2):
    return np.linalg.norm(point1 - point2)

def find_start_end_frames(track_idx, locations):
    start_frame, end_frame = None, None
    frame_count = locations.shape[0]
    for frame_idx in range(frame_count):
        if not np.all(np.isnan(locations[frame_idx, :, :, track_idx])):
            end_frame = frame_idx
            if start_frame is None:
                start_frame = frame_idx
    return start_frame, end_frame

def generate_connected_track_name(track_chain):
    return "_".join(track_chain)

def circle_check(last_point, points, radius):
    for point in points:
        if calculate_distance(last_point, point) < radius:
            return True
    return False

def connect_broken_tracks(broken_tracks, not_real_tracks, frame_threshold, distance_threshold, radius, filled_locations, track_names, frame_count):
    connections = []
    remaining_broken_tracks = broken_tracks.copy()
    connected_tracks = set()
    completed_tracks = []
    track_chains = {track: [track] for track in broken_tracks}

    while remaining_broken_tracks:
        new_connections = []
        for track1_name, (start1, end1) in list(remaining_broken_tracks.items()):
            if track1_name in connected_tracks:
                continue
            best_candidate = None
            best_suitability_score = float('inf')
            for track2_name, (start2, end2) in not_real_tracks.items():
                for frame_offset in range(-10, frame_threshold + 1):  # Allowing overlap with negative frame differences
                    frame_diff = (start2 - end1) + frame_offset
                    if -(frame_threshold / 2) < frame_diff <= frame_threshold:
                        if track1_name in track_names:
                            track1_idx = track_names.index(track1_name)
                        else:
                            continue
                        track2_idx = track_names.index(track2_name)
                        track1_locations = filled_locations[:, :, :, track1_idx]
                        track2_locations = filled_locations[:, :, :, track2_idx]
                        last_point_track1 = track1_locations[end1, 0]
                        first_point_track2 = track2_locations[start2, 0]
                        spatial_distance = calculate_distance(last_point_track1, first_point_track2)
                        if spatial_distance <= distance_threshold:
                            points_in_radius = [track2_locations[start2 + i, 0] for i in range(-radius, radius + 1) if 0 <= start2 + i < filled_locations.shape[0]]
                            if circle_check(last_point_track1, points_in_radius, radius):
                                suitability_score = frame_diff + spatial_distance
                                if suitability_score < best_suitability_score:
                                    best_candidate = (track2_name, start2, end2)
                                    best_suitability_score = suitability_score
            if best_candidate:
                print(f"Connecting {track1_name} (end frame {end1}) with {best_candidate[0]} (start frame {best_candidate[1]})")
                new_connections.append((track1_name, start1, end1, best_candidate[0], best_candidate[1], best_candidate[2]))
                not_real_tracks.pop(best_candidate[0])  # Remove connected track from not_real_tracks
                connected_tracks.add(track1_name)
                track_chains[track1_name].append(best_candidate[0])
                if best_candidate[2] == frame_count - 1:  # If the connected track ends at end_frame
                    completed_tracks.append(generate_connected_track_name(track_chains[track1_name]))

        if not new_connections:
            break
        for conn in new_connections:
            connections.append(conn)
            track1_name, start1, end1, track2_name, start2, end2 = conn
            # Update broken_tracks with new end frames
            if end2 < frame_count - 1:
                remaining_broken_tracks[track2_name] = (start2, end2)
            broken_tracks[track1_name] = (start1, end2)
        remaining_broken_tracks = {k: v for k, v in broken_tracks.items() if k in [conn[0] for conn in new_connections]}

    # Remove completed tracks from broken_tracks and not_real_tracks
    for completed_track in completed_tracks:
        for track in completed_track.split('_'):
            if track in broken_tracks:
                del broken_tracks[track]
            if track in not_real_tracks:
                del not_real_tracks[track]

    return connections, completed_tracks, track_chains

def complete_new_tracks(new_tracks, not_real_tracks, frame_threshold, distance_threshold, radius, filled_locations, track_names, frame_count, completed_tracks):
    while new_tracks:
        connections, additional_completed_tracks, track_chains = connect_broken_tracks(new_tracks, not_real_tracks, frame_threshold, distance_threshold, radius, filled_locations, track_names, frame_count)
        completed_tracks.extend(additional_completed_tracks)
        new_tracks = {k: v for k, v in create_new_tracks(connections, track_chains).items() if v[1] != frame_count - 1}
        track_names.extend(new_tracks.keys())

    return completed_tracks

def create_new_tracks(connections, track_chains):
    new_tracks = {}
    for track1_name, start1, end1, track2_name, start2, end2 in connections:
        new_track_name = generate_connected_track_name(track_chains[track1_name])
        new_tracks[new_track_name] = (start1, end2)
    return new_tracks