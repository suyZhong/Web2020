#!/bin/bash

for i in $( seq 1 100 )
do
    python NB_classifier.py --alpha $i
    python calc_diff.py
    i=$(($i+1))
done