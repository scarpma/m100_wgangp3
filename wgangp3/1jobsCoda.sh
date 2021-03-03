#!/bin/bash

#SBATCH -N 1                # 1 node
#SBATCH --ntasks-per-node=8 # 8 tasks out of 32
#SBATCH --gres=gpu:1        # 1 gpus per node out of 4
#SBATCH --mem=100000        # memory per node out of 246000MB

#SBATCH -p m100_usr_prod
#SBATCH --time 24:00:00
#SBATCH -A IscrB_DRHEOB
#SBATCH --job-name=wgan-3ch
#SBATCH --mail-type=ALL
#SBATCH --mail-user=fabio.bonaccorso@roma2.infn.it,michele.buzzicotti@roma2.infn.it



module load profile/deeplrn
module load wmlce/1.6.2


export CUDA_VISIBLE_DEVICES=0
#start
#python wgan.py --gen_iters 8000 --ncritic 30 --batch_size 500 --gen_lr 0.00005 --critic_lr 0.0001 --set_train 4 --set_run 1 &
#restart 1
#python wgan.py --gen_iters 8000 --ncritic 30 --batch_size 500 --gen_lr 0.000025 --critic_lr 0.00005 --set_train 4 --load 1 8000 --set_run 2 &
#restart 2
python wgan.py --gen_iters 3000 --ncritic 30 --batch_size 1000 --gen_lr 0.000025 --critic_lr 0.00005 --set_train 4 --load 2 8000 --set_run 3 &&
python wgan.py --gen_iters 2000 --ncritic 30 --batch_size 1000 --gen_lr 0.0000025 --critic_lr 0.000005 --set_train 4 --load 3 3000 --set_run 4 &


wait # Waits for background jobs to finish ....


#python wgan.py --gen_iters 5000 --ncritic 5 --load 39 1000
# >& log.txt &
# tail -f log.txt
