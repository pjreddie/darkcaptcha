#!/bin/bash
#$ -S /bin/bash
#$ -j y
#source /homes/grail/pjreddie/.bash_profile
echo Running on host: `hostname`.
cd /homes/grail/pjreddie/darkcaptcha
python generate.py 100000 /projects/grail/unikitty/captcha

