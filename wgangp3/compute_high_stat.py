#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.insert(0, '.')
sys.path.insert(0, '..')

import os
import os.path as osp

import subprocess as sp
from params import *

from db_utils import *
import stats

#from datetime import datetime
#now = datetime.now()
#dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("ESECUZIONE: ", dt_string, "\n")

if "-h" in sys.argv:
    print("usage: plot_pdfs.py <train> <run> <number> <job_id>")
    exit()

#Read from command line input parameter
train  = int(sys.argv.pop(1))
run    = int(sys.argv.pop(1))
number = int(sys.argv.pop(1))
job_id = int(sys.argv.pop(1))

#Defines number of iterations each generating 50k trajs
iters  = 50

semidisp = (DB_MAX - DB_MIN)/2.
media = (DB_MAX + DB_MIN)/2.


save_path = f'runs/TRAIN{train}/{run}/HighStat'
if not osp.exists(save_path):
    os.makedirs(save_path)

#Define Output PDF files
save_pdf = save_path+f'/pdf_{number}_me_{job_id}.dat'

#Define Output SF files
save_sf  = save_path+f'/sf_{number}_me_{job_id}.dat'


#Load Model
path = f'runs/TRAIN{train}/{run}/{number}_gen.h5'
print('Loading Model ...')
gen = load_model(path)


#Main Loop
for i in range(iters):

    print(f"Iteration n: {i}")

    #Generate 50k Trajectories
    print("\tGenerating trajs ... ",end="")
    bs = 50000
    velo = np.zeros(shape=(bs,SIG_LEN,CHANNELS))
    print('Generating Trajectories ...')
    # noise = np.random.normal(0, 1, size=(bs, NOISE_DIM)) #VAR
    noise = np.random.standard_t(4, size=(bs, NOISE_DIM)) #VAR
    velo[:,:,COMPONENTS] = gen.predict(noise, verbose=1, batch_size=bs)
    #Renormalize in the original range
    velo = velo * semidisp + media

    #Remove Borders
    velo = velo[:,100:1900,:] # WE WITHOUT EXTREMES

    #Compute first der
    acce = np.gradient(velo,axis=1)

    print("done.")

    #Compute histo
    print('Computing Histo ...')

    #Define Output PDF bins
    nbins=600
    tmp_hist_vex, bin_ve = np.histogram(velo[:,:,0].flatten(), nbins, (-12,12), density=False)
    tmp_hist_acx, bin_ac = np.histogram(acce[:,:,0].flatten(), nbins, (-6,6),   density=False)
    tmp_hist_vey, bin_ve = np.histogram(velo[:,:,1].flatten(), nbins, (-12,12), density=False)
    tmp_hist_acy, bin_ac = np.histogram(acce[:,:,1].flatten(), nbins, (-6,6),   density=False)
    tmp_hist_vez, bin_ve = np.histogram(velo[:,:,2].flatten(), nbins, (-12,12), density=False)
    tmp_hist_acz, bin_ac = np.histogram(acce[:,:,2].flatten(), nbins, (-6,6),   density=False)

    #Compute SF
    print('Computing SF ...')
    tmp_sf = stats.compute_sf_mixed(velo)

    if i == 0:
        #Store histo
        hist_vex = tmp_hist_vex
        hist_acx = tmp_hist_acx
        hist_vey = tmp_hist_vey
        hist_acy = tmp_hist_acy
        hist_vez = tmp_hist_vez
        hist_acz = tmp_hist_acz
        #Store SF
        sfg      = tmp_sf
    else:
        #Store histo
        hist_vex = hist_vex + tmp_hist_vex
        hist_acx = hist_acx + tmp_hist_acx
        hist_vey = hist_vey + tmp_hist_vey
        hist_acy = hist_acy + tmp_hist_acy
        hist_vez = hist_vez + tmp_hist_vez
        hist_acz = hist_acz + tmp_hist_acz

        #Store SF
        sfg[:,1:] = sfg[:,1:] + tmp_sf[:,1:]



#Write Histo tot
array_to_save = np.stack((bin_ve[:-1],hist_vex,hist_vey,hist_vez,
                          bin_ac[:-1],hist_acx,hist_acy,hist_acz)).T


np.savetxt(save_pdf, array_to_save)


#Write SF tot
sfg[:,1:] = sfg[:,1:] / iters
np.savetxt(save_sf, sfg)

