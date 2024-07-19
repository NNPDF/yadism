In order to compute all the N3LO grids run
```
python produce_grids.py
for nf in 3 4 5; do for kind in 2 L ; do for channel in g q ; do python yad_grids.py $nf 4 $kind $channel 3 gm ; done ; done ; done
```
