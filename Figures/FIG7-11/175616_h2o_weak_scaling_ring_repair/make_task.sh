#!/usr/bin/env bash
set -euo pipefail

base_ngpu=1
base_rx=7
base_ry=7
base_rz=7

for ngpu in 2 4 8 16
do
  nnode=$((8*${ngpu}))
  ntask=4
  nproc=${ngpu}

  # how many times ngpu doubled relative to base_ngpu
  tmp=$(( ngpu / base_ngpu ))
  k=0
  while (( tmp > 1 )); do
    tmp=$(( tmp / 2 ))
    k=$(( k + 1 ))
  done

  rx=$base_rx
  ry=$base_ry
  rz=$base_rz

  # each doubling step doubles one dimension: x, then y, then z, repeat
  for ((j=0; j<k; j++)); do
    case $(( j % 3 )) in
      0) rx=$(( rx * 2 )) ;;
      1) ry=$(( ry * 2 )) ;;
      2) rz=$(( rz * 2 )) ;;
    esac
  done

  echo "ngpu=${ngpu} nnode=${nnode} ntask=${ntask} replicate=${rx} ${ry} ${rz}"

  dir_=${ngpu}gpu
  cp -r template_task "${dir_}"
  cd "${dir_}"

  sed -i "s/NNODE/${nnode}/g" run.slurm
  sed -i "s/NTASK/${ntask}/g" run.slurm
  sed -i "s/NPROC/${nproc}/g" run.slurm

  # Update replicate line in in.lammps
  sed -i "s/^replicate[[:space:]].*/replicate       ${rx} ${ry} ${rz}/" in.lammps

  sbatch run.slurm
  cd ..
done
