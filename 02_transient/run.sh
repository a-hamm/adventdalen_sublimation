rm *.xmf *.h5 log.log
#echo "start" > time.log
#date >> time.log
#which mpirun >> time.log
time ats --xml_file="columnBo.xml" --verbosity="high" 1> log.log 
#echo "end" >> time.log
#date >> time.log
