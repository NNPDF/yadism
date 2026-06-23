#!/bin/bash

cores=4
order=3

for nf in 3 4 5; do
    for kind in 2 L; do
        for channel in g q; do
            python yad_grids.py $nf $cores $kind $channel $order;
        done
    done
done
