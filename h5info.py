import h5py

# Load the .h5 file to inspect its structure
file_path = '7_3_dev.h5'

with h5py.File(file_path, 'r') as h5_file:
    # Get the structure of the HDF5 file
    structure = {key: type(h5_file[key]) for key in h5_file.keys()}
    structure_details = {key: list(h5_file[key].attrs.keys()) for key in h5_file.keys()}

structure, structure_details

# Extracting the contents of each dataset to provide a summary of the data
with h5py.File(file_path, 'r') as h5_file:
    data_summary = {key: h5_file[key][()] if key in h5_file else None for key in h5_file.keys()}

data_summary

# Displaying a formatted version of the data directly to the terminal
for key, value in data_summary.items():
    print(f"{key}:")
    if isinstance(value, (bytes, str)):
        print(f"  {value}\n")
    elif isinstance(value, (list, tuple, dict)):
        print(f"  {value}\n")
    elif isinstance(value, (int, float)):
        print(f"  {value}\n")
    else:  # For large arrays, display only a summary
        print(f"  Shape: {value.shape} | Type: {value.dtype}\n")

print("Data summary printed to terminal.")

"""
edge_inds:
  Shape: (2, 2) | Type: int32

edge_names:
  Shape: (2, 2) | Type: |S11

instance_scores:
  Shape: (50, 4976) | Type: float64

labels_path:
  b'//gfs05/g15/410SERV/AG0 McMahon/\xc3\x96zge/cutting_legs/slp/7_3_flow_centroid_H_dev.slp'

node_names:
  Shape: (3,) | Type: |S11

point_scores:
  Shape: (50, 3, 4976) | Type: float64

provenance:
  b'{"model_paths": ["/home/okilic/models/baseline.centroid_2/training_config.json", "/home/okilic/models/baseline_medium_rf.topdown_3/training_config.json"], "predictor": "TopDownPredictor", "sleap_version": "1.4.1a2", "platform": "Linux-5.10.0-30-amd64-x86_64-with-debian-11.10", "command": "/home/okilic/mambaforge/envs/sleap_dev/bin/sleap-track /home/okilic/cutting_legs/C-/3/C-_7_3_5000_21.03.240.mp4 -m /home/okilic/models/baseline.centroid_2/ -m /home/okilic/models/baseline_medium_rf.topdown_3/ --tracking.tracker flow --tracking.similarity centroid --tracking.match hungarian --tracking.track_window 20 -o /home/okilic/cutting_legs/tracked/7_3_flow_centroid_H_dev.slp --cpu", "data_path": "/home/okilic/cutting_legs/C-/3/C-_7_3_5000_21.03.240.mp4", "output_path": "/home/okilic/cutting_legs/tracked/7_3_flow_centroid_H_dev.slp", "total_elapsed": 11489.714388847351, "start_timestamp": "2024-10-01 11:05:03.220397", "finish_timestamp": "2024-10-01 14:16:32.934752", "args": {"data_path": "/home/okilic/cutting_legs/C-/3/C-_7_3_5000_21.03.240.mp4", "models": ["/home/okilic/models/baseline.centroid_2/", "/home/okilic/models/baseline_medium_rf.topdown_3/"], "frames": "", "only_labeled_frames": false, "only_suggested_frames": false, "output": "/home/okilic/cutting_legs/tracked/7_3_flow_centroid_H_dev.slp", "no_empty_frames": false, "verbosity": "rich", "video.dataset": null, "video.input_format": "channels_last", "video.index": "", "cpu": true, "first_gpu": false, "last_gpu": false, "gpu": "auto", "max_edge_length_ratio": 0.25, "dist_penalty_weight": 1.0, "batch_size": 4, "open_in_gui": false, "peak_threshold": 0.2, "max_instances": null, "tracking.tracker": "flow", "tracking.max_tracking": null, "tracking.max_tracks": null, "tracking.target_instance_count": null, "tracking.pre_cull_to_target": null, "tracking.pre_cull_iou_threshold": null, "tracking.post_connect_single_breaks": null, "tracking.clean_instance_count": null, "tracking.clean_iou_threshold": null, "tracking.similarity": "centroid", "tracking.match": "hungarian", "tracking.robust": null, "tracking.track_window": 20, "tracking.min_new_track_points": null, "tracking.min_match_points": null, "tracking.img_scale": null, "tracking.of_window_size": null, "tracking.of_max_levels": null, "tracking.save_shifted_instances": null, "tracking.kf_node_indices": null, "tracking.kf_init_frame_count": null, "tracking.oks_errors": null, "tracking.oks_score_weighting": null, "tracking.oks_normalization": null}}'

track_names:
  Shape: (50,) | Type: |S11

track_occupancy:
  Shape: (4976, 50) | Type: uint8

tracking_scores:
  Shape: (50, 4976) | Type: float64

tracks:
  Shape: (50, 2, 3, 4976) | Type: float64

video_ind:
  Shape: () | Type: int32

video_path:
  b'//gfs05/g15/410SERV/AG0 McMahon/\xc3\x96zge/cutting_legs/C-/3/C-_7_3_5000_21.03.240.mp4'

Data summary printed to terminal.
"""
