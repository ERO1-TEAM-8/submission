echo "Step 1: Drone simulation: processing......"

chmod u+x  drone_simulation.sh

cd ../drone 

#Replace the python path with your local environment path 
if [[ "$CONDA_DEFAULT_ENV" != "ox" ]]; then
    conda activate ox
fi
#python3
#python
/Users/ahmadharkous/opt/anaconda3/envs/ox/bin/python /Users/ahmadharkous/Desktop/s6-ing/ERO1/submission/drone/main.py
#python3 main.py

echo "Opening the Graph ......"

open index.html