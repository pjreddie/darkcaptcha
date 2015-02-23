#!/bin/bash

N=$1
for ((i=0; i<$N; i++))
do
        qsub -q all.q ./wrapper.sh 
done
