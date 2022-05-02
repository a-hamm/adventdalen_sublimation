#!/bin/bash
run=$1
verbosity=$2
#rm *.xmf *.h5 log.log
cd $run
rm *
time ats --xml_file="../${run}.xml" --verbosity="$verbosity" 1> log.log 
