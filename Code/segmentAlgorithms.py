import numpy as np


def notes_segmentation(signal_len, fs, window_seconds, overlap_seconds):
    n_samples = int(fs * window_seconds)      # 30 ms for each window
    n_overlap = int(fs * overlap_seconds)

    i = 0
    segments = []

    while True:
        if (i + n_samples) < signal_len:
            segments.append([i, i + n_samples])
            i += n_overlap
        else:
            break

    return segments


    


