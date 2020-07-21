# AUTOGENERATED! DO NOT EDIT! File to edit: 20_surprise.processing.ipynb (unless otherwise specified).

__all__ = ['prior_p_m_num', 'prior_p_m_denum', 'p_d', 'p_d_m', 'summing_function', 'surprise']

# Cell
from functools import partial
import numpy as np
from sklearn.decomposition import PCA
from sklearn import cluster
import scipy.ndimage as ndimage
import scipy.signal as signal
import scipy as sp
from cmath import *
import itertools
import random

from ..core import *
from ..utils import *
from ..modelling import *

# Cell
def prior_p_m_num(window,seq):
    ''' it calculates the numerator of the prior'''
    ms=seq.size
    counter=0
    for i in range(window.size+1):
        if i>=ms:
            comp=window[i-ms:i]==seq
            if comp.all():
                counter+=1
    return counter

def prior_p_m_denum(window,seq):   #window is size w and seq is size ms
    ''' it calculates the denumerator of the prior'''
    return window.size-seq.size-1

def p_d(window, D):
    ''' it calculates the evidence'''
    return window[window==D].size/len(window)

def p_d_m(window,seq, D):
    ''' it calculates the likelihood'''
    ms=seq.size
    count=0
    for i in np.where(window==D)[0]:
        if i-ms>=0:
            comp=window[i-ms:i]==seq
            if comp.all():
                count+=1
    return count/prior_p_m_num(window,seq)

def summing_function(window,D,ms):
    '''it finds all the possible stataes sequences to sum across'''
    Ms=[]
    for j in np.where(window==D)[0]:
        if len(window[j-ms:j])==ms:
            Ms.append(window[j-ms:j])
    #return np.unique(np.array(Ms),axis=0)
    return np.array(Ms)


def surprise(array, window_lenght, ms):
    '''changes the trace of a pixel values according to how surprising they are'''
    filtered_array=np.zeros((len(array)))
    for time, value in enumerate(array):
        if time<window_lenght:
            filtered_array[time]=value
        else:
            Ms=summing_function(array[time-window_lenght:time],value, ms)
            if Ms.size ==0:
                surprise=1
            else:
                Ms=np.unique(Ms,axis=0)
                surprise=0
                for M in Ms:
                    likelihood=p_d_m(array[time-window_lenght:time],M, value)
                    p_m=prior_p_m_num(array[time-window_lenght:time],M)/prior_p_m_denum(array[time-window_lenght:time],M)
                    posterior=likelihood*p_m/p_d(array[time-window_lenght:time],value)
                    surprise+=posterior*np.log(posterior/p_m)
            filtered_array[time]=surprise
    return filtered_array