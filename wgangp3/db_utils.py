#!/usr/bin/env python
# coding: utf-8

from params import *
import os
import os.path
import subprocess
import sys
sys.path.insert(0, '.')
sys.path.insert(0, '..')
import glob
import argparse
import stats

import tensorflow
import tensorflow.keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.initializers import RandomNormal
from tensorflow.keras.regularizers import l2, l1
from tensorflow.keras.layers import (Dense, Conv1D, Conv2D, Conv2DTranspose,
                                     Flatten, Dropout, ReLU, Input, Reshape,
                                     BatchNormalization, Activation, ELU, DepthwiseConv2D,
				     Concatenate)
from tensorflow.math import reduce_mean
from tensorflow.keras.models import Sequential, Model
import tensorflow.keras.backend as K
from tensorflow.keras.models import load_model
from functools import partial

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import scipy.ndimage as ff

def load_data(val_split):

    db = np.load(REAL_DB_PATH)[:,:,COMPONENTS]
    print(db.shape)
    M = db.max()
    m = db.min()
    print(M,m,"\n")
    semidisp = (M-m)/2.
    media = (M+m)/2.
    db = (db - media)/semidisp
    
    #APPLY SMOOTHING TO THE ORIGINAL DATASET Only IF Requested
    if SMOOTH_REAL_DB:
        db = ff.gaussian_filter1d(db, sigma=sigma_smooth_real,mode='nearest',truncate=trunc_smooth_real)

    if val_split < 1.:
        end = round(val_split * db.shape[0])
        return db[:end,:,:], db[end:,:,:]
    elif val_split == 1.0 :
        return db, None
