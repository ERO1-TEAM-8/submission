echo "Step 2: Snow simulation: processing......"

chmod u+x  snow_simulation.sh

cd ../snowremoval

if [[ "$CONDA_DEFAULT_ENV" != "ox" ]]; then
    conda activate ox
fi

/Users/ahmadharkous/opt/anaconda3/envs/ox/bin/python /Users/ahmadharkous/Desktop/s6-ing/ERO1/submission/snowremoval/main.py

echo "Opening the Graph simulation ......"
open index.html
