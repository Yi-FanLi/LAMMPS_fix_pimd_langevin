#!/bin/bash
#SBATCH --parsable
#SBATCH --account=m3538_g      #(-A, --account)
#SBATCH --constraint=gpu       #(-C, --constraint)
#SBATCH --qos=premium           #(-Q, --qos)
#SBATCH --time=47:59:00        #(-t, --time)
#SBATCH --nodes=1  #(-N, --nodes)
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:4
##SBATCH --image=docker:deepmodeling/deepmd-kit:2.2.9_cuda118
##SBATCH --image=docker:deepmodeling/deepmd-kit:2.2.7_cuda11.6_gpu

export SLURM_CPU_BIND=cores
module load python
conda activate dp-pimd-devel

i-pi input.xml &
sleep 10

for i in {0..7}; do
  gpu=$(( i % 4 ))
  echo "Launching dp_ipi $i on GPU $gpu"
  CUDA_VISIBLE_DEVICES=$gpu ./mps-wrapper.sh dp_ipi water.json &
done
wait
