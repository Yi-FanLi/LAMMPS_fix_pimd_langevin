for ngpu in 8 16
#for ngpu in 1 2 4 16 32
#for ngpu in 4
do
nnode=$(((${ngpu}+3)/4))
#nnode=$((8*${ngpu}))
#nnode=1
#ntask=$((4*${ngpu}))
#ntask=${ngpu}
ntask=4
nproc=${ngpu}
##ntask=$((32/${nnode}))
#ngpu_per_node=$((${ngpu}/${nnode}))
echo ${nnode} ${ntask} ${ngpu}
dir_=${ngpu}gpu
cp -r template_task ${dir_}
cd ${dir_}
sed -i "s/NNODE/${nnode}/g" run.slurm
sed -i "s/NTASK/${ntask}/g" run.slurm
#sed -i "s/NGPU/${ngpu_per_node}/g" run.slurm
sed -i "s/NPROC/${nproc}/g" run.slurm
sbatch run.slurm
cd ..
done
