#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.insert(0, '.')
sys.path.insert(0, '..')
import os
import os.path
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from params import *
import stats
from glob import glob
import os.path as osp



# COMMAND LINE PARSING

if "-h" in sys.argv:
    print("usage: histo_analysis.py <train> <run> <number> [--no_plot]")
    exit()

#Define as true if you wan tot average over different trainings
mean_over_train = False

train  = int(sys.argv.pop(1))
run    = int(sys.argv.pop(1))
number = int(sys.argv.pop(1))

plot = False


while len(sys.argv) > 1:
    if sys.argv[1] == '--no_plot':
        gen_renorm = plot = False
        sys.argv.pop(1)
    else:
        raise NameError('Parsing error, exiting.')
        exit()



# DEFINE SAVE FILES
if not mean_over_train:
    save_path = f'runs/TRAIN{train}/{run}/HighStat/TOT_{number}'
else:
    save_path = f'runs/TOT-STAT'
if not osp.exists(save_path):
    os.makedirs(save_path)

save_filex = osp.join(save_path, 'pdfx.dat')
save_filex_real = osp.join(save_path, 'pdfrx.dat')
#save_figurex = osp.join(save_path, 'fig_pdfx')
save_filey = osp.join(save_path, 'pdfy.dat')
save_filey_real = osp.join(save_path, 'pdfry.dat')
#save_figurey = osp.join(save_path, 'fig_pdfy')
save_filez = osp.join(save_path, 'pdfz.dat')
save_filez_real = osp.join(save_path, 'pdfrz.dat')
#save_figurez = osp.join(save_path, 'fig_pdfz')


# FIND pdf.DAT FILES
if not mean_over_train:
    read_file_gene = f'runs/TRAIN{train}/{run}/HighStat/pdf_{number}_me_*.dat'
else:
    read_file_gene = f'runs/TOT-STAT/LINKS/pdf_{number}_me_*.dat'

read_file_realx = '../data/real/pdfsx.dat'
read_file_realy = '../data/real/pdfsy.dat'
read_file_realz = '../data/real/pdfsz.dat'

read_file_gene = glob(read_file_gene)
print(f'found {len(read_file_gene)} files:')
for file in read_file_gene:
    print(file)



# READ ALREADY COMPUTED HIST
pdfrx = np.loadtxt(read_file_realx)
pdfry = np.loadtxt(read_file_realy)
pdfrz = np.loadtxt(read_file_realz)

for ii, fl in enumerate(read_file_gene):
    temp = np.loadtxt(fl)

    if ii == 0:
        vgx = temp[:,np.array([0,1])]
        vgy = temp[:,np.array([0,2])]
        vgz = temp[:,np.array([0,3])]
        agx = temp[:,np.array([4,5])]
        agy = temp[:,np.array([4,6])]
        agz = temp[:,np.array([4,7])]
        print('Reading: \t', fl)
    else:
        assert all(temp[:,0] == vgx[:,0]), 'different bin for velo'
        assert all(temp[:,4] == agx[:,0]), 'different bin for acce'
        assert all(temp[:,0] == vgy[:,0]), 'different bin for velo'
        assert all(temp[:,4] == agy[:,0]), 'different bin for acce'
        assert all(temp[:,0] == vgz[:,0]), 'different bin for velo'
        assert all(temp[:,4] == agz[:,0]), 'different bin for acce'
        vgx[:,1] = vgx[:,1] + temp[:,1]
        agx[:,1] = agx[:,1] + temp[:,5]
        vgy[:,1] = vgy[:,1] + temp[:,2]
        agy[:,1] = agy[:,1] + temp[:,6]
        vgz[:,1] = vgz[:,1] + temp[:,3]
        agz[:,1] = agz[:,1] + temp[:,7]
        print('Reading: \t', fl)


# SUM HISTOS AND COMPUTE STANDARDIZED PDF

db_vex = vgx[1,0] - vgx[0,0]
db_acx = agx[1,0] - agx[0,0]
v_normx = np.sum(vgx[:,1]) * db_vex
a_normx = np.sum(agx[:,1]) * db_acx

db_vey = vgy[1,0] - vgy[0,0]
db_acy = agy[1,0] - agy[0,0]
v_normy = np.sum(vgy[:,1]) * db_vey
a_normy = np.sum(agy[:,1]) * db_acy

db_vez = vgz[1,0] - vgz[0,0]
db_acz = agz[1,0] - agz[0,0]
v_normz = np.sum(vgz[:,1]) * db_vez
a_normz = np.sum(agz[:,1]) * db_acz

# normalize from histogram to density
vgx[:,1] = vgx[:,1] / v_normx
agx[:,1] = agx[:,1] / a_normx
vgy[:,1] = vgy[:,1] / v_normy
agy[:,1] = agy[:,1] / a_normy
vgz[:,1] = vgz[:,1] / v_normz
agz[:,1] = agz[:,1] / a_normz


# standardize
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

for jj in range(vgx.shape[0]):
    mean_vx += db_vex * vgx[jj,1]*(vgx[jj,0] + db_vex/2)
    mean_ax += db_acx * agx[jj,1]*(agx[jj,0] + db_acx/2)
    mean_vy += db_vey * vgy[jj,1]*(vgy[jj,0] + db_vey/2)
    mean_ay += db_acy * agy[jj,1]*(agy[jj,0] + db_acy/2)
    mean_vz += db_vez * vgz[jj,1]*(vgz[jj,0] + db_vez/2)
    mean_az += db_acz * agz[jj,1]*(agz[jj,0] + db_acz/2)
for jj in range(vgx.shape[0]):
    std_vx += db_vex * vgx[jj,1]*((vgx[jj,0] + db_vex/2) - mean_vx)**2.
    std_ax += db_acx * agx[jj,1]*((agx[jj,0] + db_acx/2) - mean_ax)**2.
    std_vy += db_vey * vgy[jj,1]*((vgy[jj,0] + db_vey/2) - mean_vy)**2.
    std_ay += db_acy * agy[jj,1]*((agy[jj,0] + db_acy/2) - mean_ay)**2.
    std_vz += db_vez * vgz[jj,1]*((vgz[jj,0] + db_vez/2) - mean_vz)**2.
    std_az += db_acz * agz[jj,1]*((agz[jj,0] + db_acz/2) - mean_az)**2.

std_vx = np.sqrt(std_vx)
std_ax = np.sqrt(std_ax)
std_vy = np.sqrt(std_vy)
std_ay = np.sqrt(std_ay)
std_vz = np.sqrt(std_vz)
std_az = np.sqrt(std_az)

vg_stdx = np.copy(vgx)
ag_stdx = np.copy(agx)
vg_stdy = np.copy(vgy)
ag_stdy = np.copy(agy)
vg_stdz = np.copy(vgz)
ag_stdz = np.copy(agz)

vg_stdx[:,0] = (vg_stdx[:,0] - mean_vx) / std_vx
vg_stdx[:,1] =  vg_stdx[:,1] * std_vx
ag_stdx[:,0] = (ag_stdx[:,0] - mean_ax) / std_ax
ag_stdx[:,1] =  ag_stdx[:,1] * std_ax

vg_stdy[:,0] = (vg_stdy[:,0] - mean_vy) / std_vy
vg_stdy[:,1] =  vg_stdy[:,1] * std_vy
ag_stdy[:,0] = (ag_stdy[:,0] - mean_ay) / std_ay
ag_stdy[:,1] =  ag_stdy[:,1] * std_ay

vg_stdz[:,0] = (vg_stdz[:,0] - mean_vz) / std_vz
vg_stdz[:,1] =  vg_stdz[:,1] * std_vz
ag_stdz[:,0] = (ag_stdz[:,0] - mean_az) / std_az
ag_stdz[:,1] =  ag_stdz[:,1] * std_az



# SAVE FILES

np.savetxt(save_filex, np.stack((vgx[:,0],vgx[:,1],
                                agx[:,0],agx[:,1],
                                vg_stdx[:,0],vg_stdx[:,1],
                                ag_stdx[:,0],ag_stdx[:,1])).T)
np.savetxt(save_filex_real, pdfrx)
np.savetxt(save_filey, np.stack((vgy[:,0],vgy[:,1],
                                agy[:,0],agy[:,1],
                                vg_stdy[:,0],vg_stdy[:,1],
                                ag_stdy[:,0],ag_stdy[:,1])).T)
np.savetxt(save_filey_real, pdfry)
np.savetxt(save_filez, np.stack((vgz[:,0],vgz[:,1],
                                agz[:,0],agz[:,1],
                                vg_stdz[:,0],vg_stdz[:,1],
                                ag_stdz[:,0],ag_stdz[:,1])).T)
np.savetxt(save_filez_real, pdfrz)



## # PLOT
## 
## if plot:
##     op_gen = {'marker':'.','lw':0.4,'ms':5,'label':'GAN'}
##     op_real = {'marker':'^','lw':0.4,'ms':7,'label':'DNS'}
##     op_leg = {'ncol':1}
## 
##     plt.rcParams['font.size'] = 24
##     #plt.rcParams['axes.labelweight'] = 'bold'
##     plt.rcParams['xtick.labelsize'] = 20
##     plt.rcParams['ytick.labelsize'] = 20
##     plt.rcParams['legend.fontsize'] = 17
##     #plt.rcParams['figure.titlesize'] = 22
##     plt.rcParams['figure.dpi'] = 60
##     plt.rcParams['figure.figsize'] = (17, 10)
##     #plt.rcParams['lines.linewidth'] = 0.5
##     #plt.rcParams['lines.markersize'] = 13
##     plt.rcParams['legend.markerscale'] = 2
##     #plt.rcParams['lines.marker'] = '.'
## 
##     fig, ax = plt.subplots(2,2, )
##     ax[0,1].set_yscale('log')
##     ax[1,1].set_yscale('log')
##     ax[0,0].set_xlabel('$v_x / \\sigma_{v_x}$')
##     ax[0,1].set_xlabel('$v_x / \\sigma_{v_x}$')
##     ax[1,0].set_xlabel('$a_x / \\sigma_{a_x}$')
##     ax[1,1].set_xlabel('$a_x / \\sigma_{a_x}$')
##     ax[0,0].set_ylabel('PDF$(v_x)\\cdot\\sigma_{v_x}$')
##     ax[1,0].set_ylabel('PDF$(a_x)\\cdot\\sigma_{a_x}$')
##     ax[0,0].set_xlim([-4,4])
##     ax[1,0].set_xlim([-4,4])
## 
##     # plot
##     ax[0,0].plot(*(vr), **op_real)
##     ax[0,1].plot(*(vr), **op_real)
##     ax[0,0].plot(*(vg), **op_gen)
##     ax[0,1].plot(*(vg), **op_gen)
## 
##     ax[1,0].plot(*(ar), **op_real)
##     ax[1,1].plot(*(ar), **op_real)
##     ax[1,0].plot(*(ag), **op_gen)
##     ax[1,1].plot(*(ag), **op_gen)
## 
##     # legend
##     ax[0,0].legend(**op_leg)
##     ax[0,1].legend(**op_leg)
##     ax[1,0].legend(**op_leg)
##     ax[1,1].legend(**op_leg)
## 
##     # save figure
##     fig.tight_layout()
##     fig.savefig(save_figure, fmt='png', dpi=72)
