#! /bin/bash
file1="/home/zfc/debugTool/health/REF/cpu_status_spike"
file2="/home/zfc/debugTool/health/DUT/cpu_status_haps"

 > /home/zfc/debugTool/healthReport/cpu_status_cmp_result.txt

lines=`cat $file1 | wc -l`

for i in $(seq 1 1 $lines)
do
    line1=`awk 'NR=="'$i'"{print $0}' $file1`
    line2=`awk 'NR=="'$i'"{print $0}' $file2`
    
    #echo "$i"
    #echo "$line1"
    #echo "$line2"

   # if `echo "$i" -lt 34` || `echo "$i" -gt 65` ;then
   if (("$i" < 34 )) || (("$i" > 65))
   then   
       register_file1=`echo $line1 | cut -d' ' -f1`
       register_file2=`echo $line2 | cut -d' ' -f1`

        if (( "$i" >= 127))
        then
            register_file1=`echo ${register_file1:0:9}`
            register_file2=`echo ${register_file2#*m}`
            register_file2=`echo ${register_file2:0:9}`
        fi

        register_file1_val=`echo $line1 | cut -d' ' -f2`
        register_file2_val=`echo $line2 | cut -d' ' -f2`
    else
        register_file1=`echo $line1 | cut -d' ' -f1`
        register_file2=`echo $line2 | cut -d' ' -f1`
        register_file1_val=`echo $line1 | cut -d' ' -f9`
        register_file2_val=`echo $line2 | cut -d' ' -f9`
        register_file1_val=`echo ${register_file1_val%?}`
        register_file2_val=`echo ${register_file2_val%?}`
    fi

    #if [ $register_file1 = $register_file2 ];then
        if [ $register_file1_val != $register_file2_val ];then
            #echo "$i" >> cpu_status_cmp_result.txt
            echo ""$register_file1""  """$register_file1_val""" >> /home/zfc/debugTool/healthReport/cpu_status_cmp_result.txt
            # echo "$register_file1_val"
            echo ""$register_file2""  ""$register_file2_val""  >> /home/zfc/debugTool/healthReport/cpu_status_cmp_result.txt
            # echo "$register_file2_val"
#    else
#         echo "the same value!!!!!!!!!!!!"
        fi
  # fi
done
