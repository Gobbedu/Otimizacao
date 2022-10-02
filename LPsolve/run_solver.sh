#!/bin/bash

./input.py < input1.txt > aux.lp 
./lp-solve/lp_solve aux.lp
