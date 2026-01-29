module purge
source /opt/cray/pe/cpe/23.12/restore_lmod_system_defaults.sh
module load PrgEnv-gnu cray-mpich cudatoolkit craype-accel-nvidia80 python
conda activate postproc
export SLURM_CPU_BIND=cores
