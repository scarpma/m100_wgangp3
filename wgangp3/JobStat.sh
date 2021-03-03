#!/bin/bash

#SBATCH -N 1                # 1 node
#SBATCH --ntasks-per-node=8 # 8 tasks out of 32
#SBATCH --gres=gpu:4        # 4 gpus per node out of 4
#SBATCH --mem=240000        # memory per node out of 246000MB

#SBATCH -p m100_usr_prod
#SBATCH --time 10:00:00
#SBATCH -A INF21_fldturb_0
#SBATCH --job-name=Stat
#SBATCH --mail-type=ALL
#SBATCH --mail-user=scarpma@gmail.com

# coda "bug" più veloce, ma massimo 30 min

module load profile/deeplrn
module load wmlce/1.6.2


export CUDA_VISIBLE_DEVICES=0
python compute_high_stat.py 1 4 2000 0 >& log1.txt &

export CUDA_VISIBLE_DEVICES=1
python compute_high_stat.py 2 4 2000 0 >& log2.txt &

export CUDA_VISIBLE_DEVICES=2
python compute_high_stat.py 3 4 2000 0 >& log3.txt &

export CUDA_VISIBLE_DEVICES=3
python compute_high_stat.py 4 4 2000 0 >& log4.txt &




wait # Waits for background jobs to finish ....


#python wgan.py --gen_iters 5000 --ncritic 5 --load 39 1000
# >& log.txt &
# tail -f log.txt
