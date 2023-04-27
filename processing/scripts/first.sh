#!/bin/bash
echo "setting up directories for $1 integrase"
echo "copy and paste the following line for rsync"
echo "rsync -auvz * heewhan@midway3.rcc.uchicago.edu:/beagle3/price/top_search/$1/ready"
mkdir $1
cd $1
mkdir ready msas predictions log
