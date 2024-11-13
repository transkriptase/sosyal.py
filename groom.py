import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from loadh5 import load_h5_data  # loadh5.py dosyasından import
import h5py

def calculate_angle(vector1, vector2):
    """Calculate the angle (in degrees) between two vectors."""
    unit_vector1 = vector1 / np.linalg.norm(vector1)
    unit_vector2 = vector2 / np.linalg.norm(vector2)
    dot_product = np.dot(unit_vector1, unit_vector2)
    angle = np.arccos(np.clip(dot_product, -1.0, 1.0))
    return np.degrees(angle)

def detect_grooming_events(locations, min_distance=1, max_distance=50, min_duration_frames=45):
    frame_count, body_parts, _, num_termites = locations.shape
    grooming_events = []
    MANDIBLE_INDEX = 0  # Mandible (çene) noktası
    ABDOMEN_INDEX = 2   # Abdomen noktası

    for i in range(num_termites):
        for j in range(num_termites):
            if i == j:
                continue  # Aynı termitleri atla

            start_frame = None
            duration = 0

            for frame in range(frame_count):
                mandible_i = locations[frame, MANDIBLE_INDEX, :, i]
                abdomen_j = locations[frame, ABDOMEN_INDEX, :, j]

                if np.isnan(mandible_i).any() or np.isnan(abdomen_j).any():
                    if duration >= min_duration_frames:
                        grooming_events.append((i, j, start_frame, frame - 1))
                    start_frame = None
                    duration = 0
                    continue

                distance = np.linalg.norm(mandible_i - abdomen_j)

                if min_distance <= distance <= max_distance:
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

# Grooming olaylarını görselleştirmek için zaman çizelgesi fonksiyonu
def plot_grooming_timeline(grooming_events):
    plt.figure(figsize=(15, 10))
    for event in grooming_events:
        track_a, track_b, start_frame, end_frame = event
        plt.hlines(y=f"{track_a}-{track_b}", xmin=start_frame, xmax=end_frame, linewidth=2)

    plt.title("Grooming Olayları Zaman Çizelgesi")
    plt.xlabel("Kare Numarası")
    plt.ylabel("İz Çiftleri")
    plt.grid(True)
    plt.show()