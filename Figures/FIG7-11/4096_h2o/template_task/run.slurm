#!/bin/bash
#SBATCH --parsable
#SBATCH --account=m3538_g      #(-A, --account)
#SBATCH --constraint=gpu       #(-C, --constraint)
#SBATCH --qos=premium           #(-Q, --qos)
#SBATCH --time=00:59:00        #(-t, --time)
#SBATCH --nodes=NNODE  #(-N, --nodes)
#SBATCH --ntasks-per-node=NTASK
#SBATCH --gres=gpu:NGPU
##SBATCH --image=docker:deepmodeling/deepmd-kit:3.0.3_cuda128
#SBATCH --image=docker:deepmodeling/deepmd-kit:2.2.9_cuda118
##SBATCH --image=docker:deepmodeling/deepmd-kit:2.2.7_cuda11.6_gpu

export SLURM_CPU_BIND=cores
srun --mpi=pmi2 shifter --entrypoint ./mps-wrapper.sh lmp -in in.lammps -p 32x1 -log log -screen screen
