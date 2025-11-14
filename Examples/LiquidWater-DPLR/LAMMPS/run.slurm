#!/bin/bash
#SBATCH --parsable
#SBATCH --account=xxxxxxx      #(-A, --account)
#SBATCH --constraint=gpu       #(-C, --constraint)
#SBATCH --qos=premium           #(-Q, --qos)
#SBATCH --time=23:59:00        #(-t, --time)
#SBATCH --nodes=1  #(-N, --nodes)
#SBATCH --ntasks-per-node=32
#SBATCH --gres=gpu:4

export SLURM_CPU_BIND=cores
module load python
conda activate dp-pimd-devel
srun --mpi=pmi2 ./mps-wrapper.sh lmp -in in.lammps -p 32x1 -log log -screen screen
