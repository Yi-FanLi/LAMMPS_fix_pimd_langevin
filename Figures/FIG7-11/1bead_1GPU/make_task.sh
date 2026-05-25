for nx in {5..7}
do
nH2O=$((${nx}*${nx}*${nx}*512))
echo ${nH2O}
#for ngpu in 1 2 4 16 32
#for ngpu in 4
#nnode=$(((${ngpu}+3)/4))
#ntask=$((32/${nnode}))
#ngpu_per_node=$((${ngpu}/${nnode}))
#echo ${nnode} ${ntask} ${ngpu}
dir_=${nH2O}h2o
cp -r template_task ${dir_}
cd ${dir_}
sed -i "s/NX/${nx}/g" in.lammps
sed -i "s/NY/${nx}/g" in.lammps
sed -i "s/NZ/${nx}/g" in.lammps
sbatch run.slurm
cd ..
done
