#!/bin/bash
#SBATCH --parsable
#SBATCH --account=m3538_g      #(-A, --account)
#SBATCH --constraint=gpu       #(-C, --constraint)
#SBATCH --qos=premium           #(-Q, --qos)
#SBATCH --time=00:10:00        #(-t, --time)
#SBATCH --nodes=1  #(-N, --nodes)
##SBATCH --ntasks-per-node=32
##SBATCH --gpus-per-task=1
##SBATCH --gres=gpu:4
##SBATCH --nodes=1  #(-N, --nodes)
#SBATCH --ntasks-per-node=32
#SBATCH --gres=gpu:4

export SLURM_CPU_BIND=cores
module load python
conda activate dp-pimd-devel
srun --mpi=pmi2 --gpu-bind=map_gpu:0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3 ./mps-wrapper.sh lmp -in in.lammps -p 32x1 -log log -screen screen
