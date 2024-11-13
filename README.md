"""
Here's a list of potential social behaviors of termites and how they can be analyzed using data from the `.h5` file:

### 1. **Proximity and Interaction Duration**:
   - **Description**: The duration during which two termites remain within a certain distance from each other. This can indicate social interactions or cooperative behaviors such as feeding or nest building.
   - **Calculation**: Use the coordinates of tracked points from the `.h5` file to compute distances between termites and determine how long they stay within a defined threshold.

### 2. **Grooming Behavior**:
   - **Description**: Grooming is an essential social behavior in termite colonies for maintaining hygiene and communication. Detecting when one termite approaches and stays near the abdomen or head of another for a set duration can indicate grooming.
   - **Calculation**: Analyze the distance between the mandible of one termite and the abdomen or head of another, checking if this distance stays within a defined range for a specific number of frames.

### 3. **Antennal Contact**:
   - **Description**: Termites often use their antennae to touch and sense each other, which can be a form of communication.
   - **Calculation**: Identify when the antennae (tracked as specific nodes) come close to the body or head of another termite, staying within a short distance range.

### 4. **Following Behavior**:
   - **Description**: This behavior occurs when one termite follows the movement path of another.
   - **Calculation**: Track the paths of individual termites over time to identify cases where one termite maintains a consistent distance behind another for a series of frames.

### 5. **Alignment and Group Movement**:
   - **Description**: Termites moving in the same direction or aligned in a group can indicate cooperative tasks or foraging.
   - **Calculation**: Compare the angles of movement vectors between multiple termites and identify consistent directional alignment.

### 6. **Collision or Physical Contact**:
   - **Description**: Instances where two termites come into direct contact.
   - **Calculation**: Check when the distance between two tracked termite points falls below a minimal threshold (indicating touch).

### 7. **Stationary Clustering**:
   - **Description**: A group of termites remaining within a close area for an extended period could indicate colony defense or nest-related behavior.
   - **Calculation**: Use clustering algorithms to find groups of termites that do not move significantly over time.

### Which Data from the `.h5` File Can Be Used?
- **Coordinates (`tracks`)**: The 3D array of termite positions over time, which is essential for calculating distances, angles, and movements.
- **Node Names (`node_names`)**: Helps identify specific body parts like mandibles, antennae, and abdomens.
- **Track Names (`track_names`)**: Used to differentiate between individual termites in the analysis.

With these analyses in mind, we can now create the `social_behaviors.py` file to define these behaviors and make them accessible for integration into `sosyal.py`. Shall we proceed with drafting this file?
"""



# Termite Social Behavior Analysis

This repository contains Python scripts for analyzing the social behavior of termites using `.h5` data files. The project focuses on loading, cleaning, and analyzing termite tracking data to detect interactions and grooming events.

## Project Structure

- **sosyal.py**: Main script for analyzing termite social interactions.
- **fillmissing.py**: Script for handling missing data using interpolation.
- **cleaning.py**: Contains functions for cleaning and validating data.
- **connect_broken_tracks.py**: Connects broken tracks and computes distances.
- **groom.py**: Detects grooming events and visualizes them.
- **loadh5.py**: Utility for loading and inspecting `.h5` data files.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/termite-analysis.git
    cd termite-analysis
    ```

2. **Install dependencies**:
    Make sure you have Python 3.x installed. You may need the following libraries:
    ```bash
    pip install numpy h5py matplotlib scipy seaborn
    ```

## Usage

### 1. Analyzing Termite Interactions (`sosyal.py`)
This script loads `.h5` data and identifies social interactions among termites based on distance, angle, and duration criteria.

Run the script:
```bash
python sosyal.py
```

### 2. Detecting Grooming Events (`groom.py`)
Detect grooming events using the following:
```bash
python groom.py
```

### 3. Filling Missing Data (`fillmissing.py`)
The `fill_missing` function is used to fill missing data in termite locations:
```python
from fillmissing import fill_missing
```

### 4. Connecting Broken Tracks (`connect_broken_tracks.py`)
Connect broken tracks in the dataset:
```python
from connect_broken_tracks import connect_broken_tracks
```

## File Descriptions

- **sosyal.py**: Main code for analyzing interactions with functions for angle calculation and proximity analysis.
- **fillmissing.py**: Provides `fill_missing` for data interpolation.
- **cleaning.py**: Validates data quality and handles missing or invalid data points.
- **connect_broken_tracks.py**: Connects broken tracks and calculates distances.
- **groom.py**: Detects and visualizes grooming behavior among termites.
- **loadh5.py**: Loads and inspects `.h5` files.

## Example Output

Example of detected interactions printed by `sosyal.py`:
```
Detected Interactions (with distance and time filters):
Termites 0 and 1 interacted between frames 100 and 200
Termites 2 and 3 interacted between frames 350 and 450
```

## Contributing

Feel free to contribute by forking the repository and submitting pull requests.

## License

This project is licensed under the MIT License.
