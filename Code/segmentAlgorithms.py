import numpy as np
import pandas as pd


def notes_segmentation(signal_len, fs, window_seconds, overlap_seconds):
    n_samples = int(fs * window_seconds)      # 32 ms for each window
    n_overlap = int(fs * overlap_seconds)     # 10 ms for overlap
    
    n_max_freq = int(fs/500)
    
    # df=pd.DataFrame(vda_segs)
    # voice_segs=df[df[0] != "noEnergy"].to_numpy()
    # dim=voice_segs.shape

    i = 0
    segments = []

    while True:
      
        if (i + n_samples + n_max_freq) < signal_len:
            segments.append([i, i + n_samples+n_max_freq])
            i += n_overlap
        else:
            break
    return segments



    


