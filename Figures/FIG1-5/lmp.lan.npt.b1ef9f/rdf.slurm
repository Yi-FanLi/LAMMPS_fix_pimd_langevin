#!/bin/bash
#SBATCH --parsable
#SBATCH --account=m3538      #(-A, --account)
#SBATCH --constraint=gpu       #(-C, --constraint)
#SBATCH --qos=premium           #(-Q, --qos)
#SBATCH --time=00:59:00        #(-t, --time)
#SBATCH --nodes=1  #(-N, --nodes)
#SBATCH --ntasks-per-node=32

module purge
source /opt/cray/pe/cpe/23.12/restore_lmod_system_defaults.sh
module load PrgEnv-gnu cray-mpich cudatoolkit craype-accel-nvidia80 python
conda activate postproc
export SLURM_CPU_BIND=cores
srun -n 32 rdf --dir . --atype 1 1 --nbin 150
srun -n 32 rdf --dir . --atype 1 2 --nbin 150
srun -n 32 rdf --dir . --atype 2 2 --nbin 150
