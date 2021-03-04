import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    'train',
    action='store',
    help='train',
)
parser.add_argument(
    'run',
    action='store',
    help='run',
)
parser.add_argument(
    'number',
    action='store',
    help='number',
)
parser.add_argument(
    '--no_pdf',
    action='store_true',
    default=False,
    help='do not plot pdfs',
)
parser.add_argument(
    '--no_sf',
    action='store_true',
    default=False,
    help='do not plot structure functions',
)
args = parser.parse_args()


plt.rcParams['font.size'] =15
#plt.rcParams['xtick.labelsize'] = 20
#plt.rcParams['ytick.labelsize'] = 20
#plt.rcParams['legend.fontsize'] = 17
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['legend.markerscale'] = 2

path = f'runs/TRAIN{args.train}/{args.run}/HighStat/TOT_{args.number}/'

if not args.no_sf:
    print("load sf files")
    sfg_file = path+'sfg.dat'
    sfr_file = path+'sfr.dat'
    sfg = np.loadtxt(sfg_file)
    sfr = np.loadtxt(sfr_file)
    dlg_file = path+'dlg.dat'
    dlr_file = path+'dlr.dat'
    dlg = np.loadtxt(dlg_file)
    dlr = np.loadtxt(dlr_file)

if not args.no_pdf:
    print("load pdf files")
    pdfgx_file = path+'pdfx.dat'
    pdfrx_file = path+'pdfrx.dat'
    pdfgx = np.loadtxt(pdfgx_file)
    pdfrx = np.loadtxt(pdfrx_file)
    pdfgy_file = path+'pdfy.dat'
    pdfry_file = path+'pdfry.dat'
    pdfgy = np.loadtxt(pdfgy_file)
    pdfry = np.loadtxt(pdfry_file)
    pdfgz_file = path+'pdfz.dat'
    pdfrz_file = path+'pdfrz.dat'
    pdfgz = np.loadtxt(pdfgz_file)
    pdfrz = np.loadtxt(pdfrz_file)

# plot params
op_gen   = {'marker':'.','lw':0.4,'ms':5,'label':'GAN', 'c':'C1'}
op_real  = {'marker':'^','lw':0.4,'ms':6,'label':'DNS', 'c':'C0'}
op_gen2  = {'marker':'.','lw':0.4,'ms':5,}
op_real2 = {'marker':'^','lw':0.4,'ms':7,}
op_leg   = {'markerscale':1, 'ncol':1}


if not args.no_pdf:
    print('plot pdf')
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
    fig.savefig(path+'pdfx.png')


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
    fig.savefig(path+'pdfy.png')



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
    fig.savefig(path+'pdfz.png')





if not args.no_sf:
    print('plot sf')
    fig, ax = plt.subplots(1,2, )
    # sf ordine 2  longitudinali e ordine 4 trasversali 
    ax[0].set_xlabel('$\\tau$')
    ax[0].set_ylabel('$S_p(\\tau)$')
    ax[0].set_yscale('log')
    ax[0].set_xscale('log')
    ax[0].plot(sfr[:,0], sfr[:,1], **op_real2, c='C0', label='p=xx DNS')    # <dux**2>
    ax[0].plot(sfg[:,0], sfg[:,1], **op_gen2 , c='C1', label='p=xx GAN')
    ax[0].plot(sfr[:,0], sfr[:,4], **op_real2, c='C2', label='p=xxyy DNS')  # <dux**2 * duy**2>
    ax[0].plot(sfg[:,0], sfg[:,4], **op_gen2 , c='C3', label='p=xxyy GAN')
    ax[0].legend(**op_leg)
    # derivata logaritmica sf ordine 2  longitudinali e ordine 4 trasversali
    ax[1].set_xlabel('$\\tau$')
    ax[1].set_ylabel('$D S_p(\\tau)$')
    ax[1].set_xscale('log')
    ax[1].plot(dlr[:,0], dlr[:,1], **op_real2, c='C0', label='p=xx DNS')    # <dux**2>
    ax[1].plot(dlg[:,0], dlg[:,1], **op_gen2 , c='C1', label='p=xx GAN')
    ax[1].plot(dlr[:,0], dlr[:,4], **op_real2, c='C2', label='p=xxyy DNS')  # <dux**2 * duy**2>
    ax[1].plot(dlg[:,0], dlg[:,4], **op_gen2 , c='C3', label='p=xxyy GAN')
    ax[1].legend(**op_leg)

    fig.suptitle('F_2$ and $D SF_4$')
    fig.tight_layout()
    fig.savefig(path+'sf.png')

    # correlazione <dux**2 * duy**2> / (<dux**2> * <duy**2>)
    fig, ax = plt.subplots(1,1, figsize=(7,5))
    ax.set_xlabel('$\\tau$')
    ax.set_xscale('log')
    ax.plot(sfr[:,0], sfr[:,4]/(sfr[:,1]*sfr[:,2]), **op_real)
    ax.plot(sfg[:,0], sfg[:,4]/(sfg[:,1]*sfg[:,2]), **op_gen )
    ax.legend(**op_leg)

    fig.suptitle('$<\\delta u_x^2 \\delta u_y^2> / (<\\delta u_x^2> <\\delta u_y^2>)$')
    fig.tight_layout()
    fig.savefig(path+'corxy.png')

    # correlazione <duy**2 * duz**2> / (<duy**2> * <duz**2>)
    fig, ax = plt.subplots(1,1, figsize=(7,5))
    ax.set_xlabel('$\\tau$')
    ax.set_xscale('log')
    ax.plot(sfr[:,0], sfr[:,5]/(sfr[:,2]*sfr[:,3]), **op_real)
    ax.plot(sfg[:,0], sfg[:,5]/(sfg[:,2]*sfg[:,3]), **op_gen )
    ax.legend(**op_leg)

    fig.suptitle('$<\\delta u_y^2 \\delta u_z^2> / (<\\delta u_y^2> <\\delta u_z^2>)$')
    fig.tight_layout()
    fig.savefig(path+'coryz.png')

    # correlazione <dux**2 * duz**2> / (<dux**2> * <duz**2>)
    fig, ax = plt.subplots(1,1, figsize=(7,5))
    ax.set_xlabel('$\\tau$')
    ax.set_xscale('log')
    ax.plot(sfr[:,0], sfr[:,5]/(sfr[:,1]*sfr[:,3]), **op_real)
    ax.plot(sfg[:,0], sfg[:,5]/(sfg[:,1]*sfg[:,3]), **op_gen )
    ax.legend(**op_leg)

    fig.suptitle('$<\\delta u_x^2 \\delta u_z^2> / (<\\delta u_x^2> <\\delta u_z^2>)$')
    fig.tight_layout()
    fig.savefig(path+'corxz.png')
