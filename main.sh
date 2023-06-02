#!/bin/bash
chmod u+x main.sh

# Check if pip is installed
pip --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Error: pip is not installed. Please install it and try again."
    exit 1
fi

# Install the requirements
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Requirement instalation failed."
    exit 1
fi

# Parse command line arguments
if [ $# -eq 0 ]; then
    echo "Error: No simulation type specified. Please provide either 'drone' or 'snow_removal' as an argument."
    exit 1
fi

simulation_type=$1

if [ "$simulation_type" = "drone" ]; then
    ./scripts/drone_simulation.sh 
elif [ "$simulation_type" = "snow_removal" ]; then
    ./scripts/snow_removal_simulation.sh
else
    echo "Error: Unknown simulation type. Please provide either 'drone' or 'snow_removal' as an argument."
    exit 1
fi
