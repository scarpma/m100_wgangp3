import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.size'] =15
#plt.rcParams['xtick.labelsize'] = 20
#plt.rcParams['ytick.labelsize'] = 20
#plt.rcParams['legend.fontsize'] = 17
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['legend.markerscale'] = 2

## sfg_file = 'sfg.dat'
## sfr_file = 'sfr.dat'
## sfg = np.loadtxt(sfg_file)
## sfr = np.loadtxt(sfr_file)

print("load files")
pdfgx_file = 'pdfx.dat'
pdfrx_file = 'pdfrx.dat'
pdfgx = np.loadtxt(pdfgx_file)
pdfrx = np.loadtxt(pdfrx_file)
pdfgy_file = 'pdfy.dat'
pdfry_file = 'pdfry.dat'
pdfgy = np.loadtxt(pdfgy_file)
pdfry = np.loadtxt(pdfry_file)
pdfgz_file = 'pdfz.dat'
pdfrz_file = 'pdfrz.dat'
pdfgz = np.loadtxt(pdfgz_file)
pdfrz = np.loadtxt(pdfrz_file)

# plot params
op_gen     = {'marker':'.','lw':0.4,'ms':5,'label':'GAN', 'c':'C1'}
op_real    = {'marker':'^','lw':0.4,'ms':6,'label':'DNS', 'c':'C0'}
op_leg     = {'markerscale':1, 'ncol':1}


print('plot')

# pdf_x plot
fig, ax = plt.subplots(1,2, )
# velo
ax[0].set_xlabel('$v_x$')
ax[0].set_ylabel('PDF$(v_x)$')
ax[0].set_yscale('log')
ax[0].plot(pdfrx[:,0], pdfrx[:,1], **op_real)
ax[0].plot(pdfgx[:,0], pdfgx[:,1], **op_gen )
ax[0].legend(**op_leg)
# acce
ax[1].set_xlabel('$a_x$')
ax[1].set_ylabel('PDF$(a_x)$')
ax[1].set_yscale('log')
ax[1].plot(pdfrx[:,2], pdfrx[:,3], **op_real)
ax[1].plot(pdfgx[:,2], pdfgx[:,3], **op_gen )
ax[1].legend(**op_leg)

fig.suptitle('PDF X')
fig.tight_layout()
fig.savefig('pdfx.png')


# pdf_y plot
fig, ax = plt.subplots(1,2, )
# velo
ax[0].set_xlabel('$v_y$')
ax[0].set_ylabel('PDF$(v_y)$')
ax[0].set_yscale('log')
ax[0].plot(pdfry[:,0], pdfry[:,1], **op_real)
ax[0].plot(pdfgy[:,0], pdfgy[:,1], **op_gen )
ax[0].legend(**op_leg)
# acce
ax[1].set_xlabel('$a_y$')
ax[1].set_ylabel('PDF$(a_y)$')
ax[1].set_yscale('log')
ax[1].plot(pdfry[:,2], pdfry[:,3], **op_real)
ax[1].plot(pdfgy[:,2], pdfgy[:,3], **op_gen )
ax[1].legend(**op_leg)

fig.suptitle('PDF Y')
fig.tight_layout()
fig.savefig('pdfy.png')





# pdf_z plot
fig, ax = plt.subplots(1,2, )
# velo
ax[0].set_xlabel('$v_z$')
ax[0].set_ylabel('PDF$(v_z)$')
ax[0].set_yscale('log')
ax[0].plot(pdfrz[:,0], pdfrz[:,1], **op_real)
ax[0].plot(pdfgz[:,0], pdfgz[:,1], **op_gen )
ax[0].legend(**op_leg)
# acce
ax[1].set_xlabel('$a_z$')
ax[1].set_ylabel('PDF$(a_z)$')
ax[1].set_yscale('log')
ax[1].plot(pdfrz[:,2], pdfrz[:,3], **op_real)
ax[1].plot(pdfgz[:,2], pdfgz[:,3], **op_gen )
ax[1].legend(**op_leg)

fig.suptitle('PDF Z')
fig.tight_layout()
fig.savefig('pdfz.png')






# sf plot ?????????????????
fig, ax = plt.subplots(1,2, )
# velo
ax[0].set_xlabel('$v_z$')
ax[0].set_ylabel('PDF$(v_z)$')
ax[0].set_yscale('log')
ax[0].plot(pdfrz[:,0], pdfrz[:,1], **op_real)
ax[0].plot(pdfgz[:,0], pdfgz[:,1], **op_gen )
ax[0].legend(**op_leg)
# acce
ax[1].set_xlabel('$a_z$')
ax[1].set_ylabel('PDF$(a_z)$')
ax[1].set_yscale('log')
ax[1].plot(pdfrz[:,2], pdfrz[:,3], **op_real)
ax[1].plot(pdfgz[:,2], pdfgz[:,3], **op_gen )
ax[1].legend(**op_leg)

fig.suptitle('PDF Z')
fig.tight_layout()
fig.savefig('pdfz.png')
