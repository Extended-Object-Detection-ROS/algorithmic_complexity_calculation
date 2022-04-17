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
    #print(df)
    #columns_num = len(df.columns)
    print(df[df[2:]])
