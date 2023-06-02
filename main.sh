 #!/bin/bash
echo -e "
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
The lines to replace are located in the main.sh file at teh root of the project:\n

line 27: source ~/opt/anaconda3/etc/profile.d/conda.sh\n
line 74: source ~/opt/anaconda3/etc/profile.d/conda.sh\n
-----------------------------------------------------\n"

read -p "Proceed (y/n)? " choice
if [[ $choice != "y" ]]; then
  echo "Exit by user choice."
  exit 1
fi


echo -e "---------------------------------------------------------------Instaling Project requirements...---------------------------------------------------------------\n"
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

echo -e "---------------------------------------------------------------Creating New Conda Environment...---------------------------------------------------------------\n"
#Create conda environment and install requirements
conda create --name $input_variable --file requirements.txt
if [ $? -ne 0 ]; then
    echo "Requirement instalation failed."
    exit 1
fi

echo -e "---------------------------------------------------------------Finishing Instaling Project requirements...---------------------------------------------------------------\n"


if [ $# -eq 0 ]; then
    echo "Error: No simulation type specified. Please provide either 'drone' or 'snow_removal' as an argument."
    echo -e "---------------------------------------------------------------Deleting conda environment and cleaning up---------------------------------------------------------------\n"
    conda deactivate 
    conda env remove --name $input_variable --yes
    exit 1
fi

simulation_type=$1

if [ "$simulation_type" = "drone" ]; then
    echo "todo"

elif [ "$simulation_type" = "snow_removal" ]; then
    echo -e "---------------------------------------------------------------Step2: Snow removal Simulation ...---------------------------------------------------------------\n"

    if [[ "$CONDA_DEFAULT_ENV" != $input_variable ]]; then
        source ~/opt/anaconda3/etc/profile.d/conda.sh   #WARNING README : replace it with your conda.sh path
        conda activate $input_variable
    fi
    echo -e "---------------------------------------------------------------Conda environment activated---------------------------------------------------------------\n"
    echo -e "Executing:\n"$(which python)" snowremoval/main.py"
    $(which python) snowremoval/main.py
    if [ $? -ne 0 ]; then
        echo -e "Command failure : Please make sure that python command path is correct and contain anconda \n.Hint: Modify the script to use python3 instead of python  or reinstall  conda ."
        echo -e "---------------------------------------------------------------Deleting conda environment and cleaning up---------------------------------------------------------------\n"
        conda deactivate 
        conda env remove --name $input_variable --yes
        exit 1
    fi
    echo -e "---------------------------------------------------------------Opening the Graph Simulation ......---------------------------------------------------------------\n"
    open network.html

else
    echo "Error: Unknown simulation type. Please provide either 'drone' or 'snow_removal' as an argument."
    exit 1
fi
echo -e "---------------------------------------------------------------Deleting conda environment and cleaning up---------------------------------------------------------------\n"
conda deactivate 

conda env remove --name $input_variable --yes
