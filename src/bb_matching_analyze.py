#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from scipy.optimize import curve_fit
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error

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
    
    #plt.title('Bb_matching algorithm time complexity')
    #plt.xlabel('Bounding box number')
    #plt.ylabel('Bounding box number')
    #plt.pcolormesh(time_means_reshaped, cmap="Reds")
    #plt.colorbar(label="ms")
    #plt.pause(1)
    
    ## curve fit
    
    # ax + by + c
    def linear_sum_func(X, a, b ,c):
        return X[0]*a + X[1]*b + c
    
    # axy + b
    def linear_mul_func(X, a, b):
        return X[0]*a*X[1] + b
    
    # x^p + y^p
    def power_sum_func(X, power):
        return np.sum(np.power(X, power), axis = 0) 
    
    # (xy)^p
    def power_mul_func(X, power):
        p = np.power(X, power)
        return p[0] * p[1]
    
    # e^c(x+y)
    def exp_sum_func(X, c):
        return np.exp(c*(X[0] + X[1]))
    
    # e^cxy
    def exp_mul_func(X, c):
        return np.exp(X[0] * X[1] * c)
        
    XY = np.array([X,Y])
    
    plot_xy = np.linspace(min_rects, max_rects, n_rects)
    plot_xy_ = np.array((plot_xy, plot_xy))
        
    plt.plot(plot_xy, np.diagonal(time_means_reshaped), label="gt")
    plt.ylim(0, np.max(time_means_reshaped))
    
    for f in [linear_sum_func, linear_mul_func, power_sum_func, power_mul_func]:#, exp_sum_func]:#, exp_mul_func]:
        popt, pcov = curve_fit(f, XY, time_means)        
        print(popt, pcov)        
        c = f(XY, *popt)        
        #r, p = pearsonr(time_means, c)        
        mse = mean_squared_error(time_means, c)
        print(mse)
        cp = f(plot_xy_, *popt)
        print('cp', cp)
        plt.plot(plot_xy, cp, ':', label=f"{mse}")
        
    for f in [power_sum_func, exp_mul_func]:
        c = f(XY, 1)
        try:
            mse = mean_squared_error(time_means, c)
        except:
            mse = -1
        print(mse)
        cp = f(plot_xy_, 1)
        print('cp', cp)
        plt.plot(plot_xy, cp, ':', label=f"{mse}")
        
    plt.legend()
    plt.show()
        
