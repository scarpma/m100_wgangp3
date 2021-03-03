#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.insert(0, '.')
sys.path.insert(0, '..')
import os
import os.path
import numpy as np
import matplotlib.pyplot as plt
from params import *
from db_utils import *
import stats
from glob import glob
import os.path as osp



# READ Real Dataset
velo = np.load(REAL_DB_PATH)[:,:,COMPONENTS]
print(velo.shape)

#APPLY SMOOTHING TO THE ORIGINAL DATASET Only IF Requested
if SMOOTH_REAL_DB:
    velo = ff.gaussian_filter1d(velo[:,:,0], sigma=sigma_smooth_real,mode='nearest',truncate=trunc_smooth_real)
    velo = np.expand_dims(velo,axis=-1)
    print("Velo shape after Smoothing ",velo.shape)


#velo = velo[0:10,:,:] # Downsize for debug

#Remove Borders
#velo = velo[:,100:1900,:] # NO FOR REAL DATA

# Compute first der
acce = np.gradient(velo,axis=1)

print("Velo and Acce Ready")


# DEFINE SAVE FILES
if not SMOOTH_REAL_DB:
    save_path = f'real'
else:
    save_path = f'real/SMOOTH-sg{sigma_smooth_real}'

if not osp.exists(save_path):
    os.makedirs(save_path)



# Compute PDF
save_file_pdfx = osp.join(save_path, 'pdfsx.dat')
save_file_pdfy = osp.join(save_path, 'pdfsy.dat')
save_file_pdfz = osp.join(save_path, 'pdfsz.dat')

nbins=600
pdf_vex, bin_ve = np.histogram(velo[:,:,0].flatten(), nbins, (-12,12), density=True)
pdf_acx, bin_ac = np.histogram(acce[:,:,0].flatten(), nbins, (-6,6),   density=True)
pdf_vey, bin_ve = np.histogram(velo[:,:,1].flatten(), nbins, (-12,12), density=True)
pdf_acy, bin_ac = np.histogram(acce[:,:,1].flatten(), nbins, (-6,6),   density=True)
pdf_vez, bin_ve = np.histogram(velo[:,:,2].flatten(), nbins, (-12,12), density=True)
pdf_acz, bin_ac = np.histogram(acce[:,:,2].flatten(), nbins, (-6,6),   density=True)



# COMPUTE  mn and sgm for STANDARDIZED PDF
mean_vx = 0.
std_vx = 0.
mean_ax = 0.
std_ax = 0.
mean_vy = 0.
std_vy = 0.
mean_ay = 0.
std_ay = 0.
mean_vz = 0.
std_vz = 0.
mean_az = 0.
std_az = 0.

mean_vx = np.mean(velo[:,:,0].flatten())
std_vx = np.std(velo[:,:,0].flatten())
mean_ax = np.mean(acce[:,:,0].flatten())
std_ax = np.std(acce[:,:,0].flatten())
mean_vy = np.mean(velo[:,:,1].flatten())
std_vy = np.std(velo[:,:,1].flatten())
mean_ay = np.mean(acce[:,:,1].flatten())
std_ay = np.std(acce[:,:,1].flatten())
mean_vz = np.mean(velo[:,:,2].flatten())
std_vz = np.std(velo[:,:,2].flatten())
mean_az = np.mean(acce[:,:,2].flatten())
std_az = np.std(acce[:,:,2].flatten())

array_to_save = np.stack((
	bin_ve[:-1],pdf_vex,
    bin_ac[:-1],pdf_acx,
    ((bin_ve[:-1] - mean_vx) / std_vx), (pdf_vex * std_vx),
    ((bin_ac[:-1] - mean_ax) / std_ax), (pdf_acx * std_ax),
)).T
np.savetxt(save_file_pdfx, array_to_save)
array_to_save = np.stack((
	bin_ve[:-1],pdf_vey,
    bin_ac[:-1],pdf_acy,
    ((bin_ve[:-1] - mean_vy) / std_vy), (pdf_vey * std_vy),
    ((bin_ac[:-1] - mean_ay) / std_ay), (pdf_acy * std_ay),
)).T
np.savetxt(save_file_pdfy, array_to_save)
array_to_save = np.stack((
	bin_ve[:-1],pdf_vez,
    bin_ac[:-1],pdf_acz,
    ((bin_ve[:-1] - mean_vz) / std_vz), (pdf_vez * std_vz),
    ((bin_ac[:-1] - mean_az) / std_az), (pdf_acz * std_az),
)).T
np.savetxt(save_file_pdfz, array_to_save)


#####################################################################
################ STRUCTURE FUNCTIONS 
#####################################################################


save_file_sfr     = osp.join(save_path, 'sfr.dat')
save_file_dlr     = osp.join(save_path, 'dlr.dat')
## save_file_ftr     = osp.join(save_path, 'ftr.dat')
## save_file_dlr_ess = osp.join(save_path, 'dlr_ess.dat')


# COMPUTE SF
sfr = stats.compute_sf_mixed(velo)


# COMPUTE LOG DERIVATIVES
dlr       = np.zeros(shape=sfr.shape)
dlr[:,0]  = sfr[:,0]
dlr[:,1:] = np.gradient( np.log(sfr[:,1:]), np.log(sfr[:,0]), axis=0 )



## # COMPUTE FLATNESS
## ftr       = np.zeros(shape=(sfr.shape[0], sfr.shape[1]-1))
## ftr[:,0]  = sfr[:,0]
## for ii in range(1, sfr.shape[1]-1):
##     ftr[:,ii] = sfr[:,ii+1] / (sfr[:,1])**(ii+1)
## 
## 
## 
## # COMPUTE LOG DERIVATIVES ESS
## dlr_ess       = np.zeros(shape=(dlr.shape[0], dlr.shape[1]-1))
## dlr_ess[:,0]  = dlr[:,0]
## for ii in range(1, sfr.shape[1]-1):
##     dlr_ess[:,ii] = dlr[:,ii+1] / dlr[:,1]



# SAVE FILES
np.savetxt(save_file_sfr, sfr)
np.savetxt(save_file_dlr, dlr)
## np.savetxt(save_file_ftr, ftr)
## np.savetxt(save_file_dlr_ess, dlr_ess )

