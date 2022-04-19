#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--file',
        help='Path to csv-file with data to process'
    )
    args = parser.parse_args()
    
    df = pd.read_csv(args.file)
    
    X = df.iloc[:,0].values            
    Y = df.iloc[:,1].values
    
    min_rects = np.min(Y)
    step_rects = np.max(Y[1:] - Y[:-1])
    max_rects = np.max(Y)
    n_rects = len([i for i in range(min_rects,max_rects,step_rects)])+1    
    
    time_part = df.iloc[:,2:].values    
    time_means = np.mean(time_part, axis = 1)    
    
    time_means_reshaped = time_means.reshape((n_rects, n_rects))    
    
    plt.title('Bb_matching algorithm time complexity')
    plt.xlabel('Bounding box number')
    plt.ylabel('Bounding box number')
    plt.pcolormesh(time_means_reshaped, cmap="Reds")
    plt.colorbar(label="ms")
    plt.show()
    
    
    
