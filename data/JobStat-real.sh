#!/bin/bash

#SBATCH -N 1                # 1 node
#SBATCH --ntasks-per-node=2 # 4 task1 out of 32
#SBATCH --gres=gpu:0        # 1 gpus per node out of 4
#SBATCH --mem=80000        # memory per node out of 246000MB

#SBATCH -p m100_usr_prod
#SBATCH --time 10:00:00
#SBATCH -A INF21_fldturb_0
#SBATCH --job-name=Stat-real
#SBATCH --mail-type=ALL
#SBATCH --mail-user=scarpma@gmail.com


module load profile/deeplrn
module load wmlce/1.6.2


python real_data_stat.py > log.out &


wait # Waits for background jobs to finish ....


#python wgan.py --gen_iters 5000 --ncritic 5 --load 39 1000
# >& log.txt &
# tail -f log.txt
