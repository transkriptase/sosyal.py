
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