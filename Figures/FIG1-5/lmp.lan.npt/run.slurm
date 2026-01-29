#!/bin/bash
#SBATCH --parsable
#SBATCH --account=m3538_g      #(-A, --account)
#SBATCH --constraint=gpu       #(-C, --constraint)
#SBATCH --qos=premium           #(-Q, --qos)
#SBATCH --time=23:59:00        #(-t, --time)
#SBATCH --nodes=1  #(-N, --nodes)
#SBATCH --ntasks-per-node=32
#SBATCH --gres=gpu:4
##SBATCH --image=docker:deepmodeling/deepmd-kit:2.2.9_cuda118
##SBATCH --image=docker:deepmodeling/deepmd-kit:2.2.7_cuda11.6_gpu

export SLURM_CPU_BIND=cores
module load python
conda activate dp-pimd-devel
#srun --mpi=pmi2 lmp -h
srun --mpi=pmi2 ./mps-wrapper.sh lmp -in in.lammps -p 32x1 -log log -screen screen
#srun --mpi=pmi2 ./mps-wrapper.sh lmp -in in.lammps -p 1x1 -log log -screen screen
