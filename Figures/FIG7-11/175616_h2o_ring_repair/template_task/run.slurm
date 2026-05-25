#!/bin/bash
#SBATCH --parsable
#SBATCH --account=m3538_g      #(-A, --account)
#SBATCH --constraint=gpu       #(-C, --constraint)
#SBATCH --qos=premium           #(-Q, --qos)
#SBATCH --time=01:59:00        #(-t, --time)
#SBATCH --nodes=NNODE  #(-N, --nodes)
#SBATCH --ntasks-per-node=NTASK
#SBATCH --gres=gpu:4
##SBATCH --image=docker:deepmodeling/deepmd-kit:3.0.3_cuda128
##SBATCH --image=docker:deepmodeling/deepmd-kit:2.2.9_cuda118
##SBATCH --image=docker:deepmodeling/deepmd-kit:2.2.7_cuda11.6_gpu

export SLURM_CPU_BIND=cores
module load python
conda activate dp-pimd-devel
srun --mpi=pmi2 lmp -in in.lammps -p 32xNPROC -log log -screen screen
