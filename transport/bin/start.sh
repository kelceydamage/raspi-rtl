echo -en "\n   +  "
for i in {0..23}; do
    printf "%2b " $i
done

for i in {0..5}; do
    let "i = i*36 +16"
    printf "\n\n %3b  " $i
    for j in {0..23}; do
        let "val = i+j"
        echo -en "\033[48;5;${val}m  \033[m "
    done
done

echo -e "\n"
echo -e "         R A S P I      (c) Robot OS                         -K. Damage\n"

local_home=`pwd`
export PATH=$local_home:$PATH
export RASPI_HOME=/git/projects/cython/personal
#export RASPI_HOME=/opt/nvme
#export RASPI_HOME=/opt
PYTHON="python"
nohup $PYTHON $RASPI_HOME/rtl/transport/bin/start.py -m 
nohup $PYTHON $RASPI_HOME/rtl/transport/bin/start.py ROUTER -a 0.0.0.0 &
nohup $PYTHON $RASPI_HOME/rtl/transport/bin/start.py CACHE -a 0.0.0.0 &
nohup $PYTHON $RASPI_HOME/rtl/transport/bin/start.py TASK -a 0.0.0.0 -p 19100 &
