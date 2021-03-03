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


import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import scipy.ndimage as ff
