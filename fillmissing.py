# -*- coding: utf-8 -*-
"""
Created on Tue May 30 23:48:39 2023

@author: okilic
"""

import h5py
import numpy as np
from scipy.interpolate import interp1d

def fill_missing(Y, kind="linear"):
    initial_shape = Y.shape
    Y = Y.reshape((initial_shape[0], -1))

    for i in range(Y.shape[-1]):
        y = Y[:, i]
        x = np.flatnonzero(~np.isnan(y))
        
        # at least 2 non-NaN values to interpolate
        if len(x) < 2:
            continue
        
        f = interp1d(x, y[x], kind=kind, fill_value=np.nan, bounds_error=False)
        xq = np.flatnonzero(np.isnan(y))
        y[xq] = f(xq)
        
        # If there are any NaN values left, fill them using linear interpolation
        mask = np.isnan(y)
        if np.any(mask):
            y[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), y[~mask])
            
        Y[:, i] = y

    Y = Y.reshape(initial_shape)
    return Y
    
def connect_and_fill(track1, track2):
    """Connect two tracks and fill in missing data."""
    combined_track = np.vstack((track1, track2))
    combined_track = combined_track[np.argsort(combined_track[:, 0])]
    all_frames = np.arange(combined_track[0, 0], combined_track[-1, 0] + 1)
    expanded_track = np.full((len(all_frames), combined_track.shape[1]), np.nan)
    expanded_track[:, 0] = all_frames
    frame_to_index = {frame: index for index, frame in enumerate(all_frames)}
    for row in combined_track:
        frame = row[0]
        expanded_track[frame_to_index[frame]] = row
    return fill_missing(expanded_track)
