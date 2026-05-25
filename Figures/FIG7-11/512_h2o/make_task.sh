for ngpu in 1 2 4 8 16 32
#for ngpu in 1 2 4 16 32
#for ngpu in 4
do
nnode=$(((${ngpu}+3)/4))
ntask=$((32/${nnode}))
ngpu_per_node=$((${ngpu}/${nnode}))
echo ${nnode} ${ntask} ${ngpu}
dir_=${ngpu}gpu
cp -r template_task ${dir_}
cd ${dir_}
sed -i "s/NNODE/${nnode}/g" run.slurm
sed -i "s/NTASK/${ntask}/g" run.slurm
sed -i "s/NGPU/${ngpu_per_node}/g" run.slurm
sbatch run.slurm
cd ..
done
