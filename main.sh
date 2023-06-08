 #!/bin/bash
if [ $# -eq 0 ]; then
    echo "Error: No simulation type specified. Please provide either 'drone' or 'snowremoval' as an argument."
    exit 1
fi
if [ $# -eq 1 ]; then
    echo "Error: No City specified. Please provide One : Sector,City,Country"
    exit 1
fi

city=$2
simulation_type=$1

printf -- "
-----------------------------------------------------
⚠️  WARNING ⚠️
-----------------------------------------------------
This script modifies your system by creating a new Conda environment.
This can potentially violate certain system constraints. 
Please ensure you have the necessary permissions and have taken necessary precautions before proceeding.
Press 'y' to continue. Press any other key to exit.



Instalation Warning:\n

You need to have conda 4.13.0 installed and added to your path.\n

Works only on macos!\n

If u want to run it on another OS:\n

You need to check the path of conda.sh and replace it in the script where there is source command\n
The lines to replace are located in the main.sh file at the root of the project:\n

line 27: source ~/opt/anaconda3/etc/profile.d/conda.sh\n
line 74: source ~/opt/anaconda3/etc/profile.d/conda.sh\n
-----------------------------------------------------\n"

read -p "Proceed (y/n)? " choice
if [[ $choice != "y" ]]; then
  echo "Exit by user choice."
  exit 1
fi


printf -- "---------------------------------------------------------------Instaling Project requirements...---------------------------------------------------------------\n"
source ~/opt/anaconda3/etc/profile.d/conda.sh

# Check if conda  is installed
conda --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Error: conda is not installed. Please install it , add it to your path and try again."
    exit 1
fi

read -p "Do you want to Create new conda env (y/n)?" CONT

if [ "$CONT" == "n" ]; then
  echo "exit";
else
  echo "Choose name"
  read input_variable

fi

printf -- "---------------------------------------------------------------Creating New Conda Environment...---------------------------------------------------------------\n"
#Check if conda environment already exists
if [[ "$CONDA_DEFAULT_ENV" == $input_variable ]]; then
    echo "Conda environment named $input_variable already exists."
else
    #Create conda environment and install requirements
    conda create --name $input_variable --file requirements.txt
    if [ $? -ne 0 ]; then
        echo "Requirement instalation failed."
        exit 1
    fi
fi


printf -- "---------------------------------------------------------------Finishing Instaling Project requirements...---------------------------------------------------------------\n"




if [[ "$simulation_type" = "snowremoval" ]] || [[ "$simulation_type" = "drone" ]]; then
    printf -- "---------------------------------------------------------------Step2: $simulation_type Simulation ...---------------------------------------------------------------\n"

    if [[ "$CONDA_DEFAULT_ENV" != $input_variable ]]; then
        source ~/opt/anaconda3/etc/profile.d/conda.sh   #WARNING README : replace it with your conda.sh path
        conda activate $input_variable
    fi
    printf -- "---------------------------------------------------------------Conda environment activated---------------------------------------------------------------\n"
    echo  "Executing:\n"$(which python)" $simulation_type/main.py $city"
    $(which python) $simulation_type/main.py $city
    if [ $? -ne 0 ]; then
        echo  "Command failure : Please make sure that python command path is correct and contain anconda \n.Hint: Modify the script to use python3 instead of python  or reinstall  conda ."
        echo  "---------------------------------------------------------------Deleting conda environment and cleaning up---------------------------------------------------------------"
        conda deactivate 
        conda env remove --name $input_variable --yes
        exit 1
    fi
    echo  "---------------------------------------------------------------Opening the Graph Simulation ......---------------------------------------------------------------"
    # open network.html if it exists
    if [[ -f "network.html" ]]; then
      open "network.html"
    fi
    
    if [[ -f "normal.png" ]]; then
      open -a "Safari" "normal.png"
    fi

    if [[ -f "opti.png" ]]; then
      open -a "Safari" "opti.png"
    fi
    if [[ -f "snowremoval.png" ]]; then
      open -a "Safari" "snowremoval.png"
    fi

    # open circuit_drone.gif in Safari if it exists
    if [[ -f "circuit_drone/gif/circuit_drone.gif" ]]; then
      open -a "Safari" "circuit_drone/gif/circuit_drone.gif"
    fi
    if [[ -f "circuit_drone2/gif/circuit_drone2.gif" ]]; then
      open -a "Safari" "circuit_drone2/gif/circuit_drone2.gif"
    fi
    if [[ -f "circuit_snow/gif/circuit_snow.gif" ]]; then
      open -a "Safari" "circuit_snow/gif/circuit_snow.gif"
    fi
    


else
    echo "Error: Unknown simulation type. Please provide either 'drone' or 'snowremoval' as an argument."
    echo "---------------------------------------------------------------Deleting conda environment and cleaning up---------------------------------------------------------------"
    conda deactivate 
    conda env remove --name $input_variable --yes
    exit 1
fi

read -p "Do you want to delete the environment , packages and network.html (y/n)? " choice
if [[ $choice != "y" ]]; then
  echo "Exit by user choice."
  exit 1
fi
echo  "---------------------------------------------------------------Deleting conda environment and cleaning up---------------------------------------------------------------"
conda deactivate  && conda env remove --name $input_variable --yes && rm -rf network.html  && rm -rf circuit_drone snowremoval.png normal.png opti.png 

#circuit_drone2 circuit_snow