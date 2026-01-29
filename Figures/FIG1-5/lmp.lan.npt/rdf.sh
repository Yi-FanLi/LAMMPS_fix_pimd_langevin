salloc -A m3538 --qos interactive --constraint cpu -N 1 -t 00:10:00 srun -n 32 rdf --dir . --atype 1 1 --nbin 150 --nsamp 2000 
salloc -A m3538 --qos interactive --constraint cpu -N 1 -t 00:10:00 srun -n 32 rdf --dir . --atype 1 2 --nbin 150 --nsamp 2000
salloc -A m3538 --qos interactive --constraint cpu -N 1 -t 00:10:00 srun -n 32 rdf --dir . --atype 2 2 --nbin 150 --nsamp 2000
