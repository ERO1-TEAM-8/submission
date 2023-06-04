# Add permission to execute the script
chmod +x main.sh
# Run Drone Simulation 
./main.sh drone

# Run Snow Removal Simulation
./main.sh snow_removal

# ⚠️ Warning
You need to have conda 4.13.0 installed and added to your path.

Works only on macos!

If u want to run it on another OS:

You need to check the path of conda.sh and replace it in the script where there is source command 

The lines to replace are located in the main.sh file at the root of the project:

line 27: source ~/opt/anaconda3/etc/profile.d/conda.sh

line 74: source ~/opt/anaconda3/etc/profile.d/conda.sh 

# Donate 
paypal.me/project_maintainer

# Snow Removal Circuit Simulation , Leynhac, France
![Alt Text](circuit_snow_removal/gif/cpp_route_animation.gif)

# Model Comparaison Drone , Outremont, Montreal, Canada , Hmmm... Why it Cost more ...?
<div >
  <img src="circuit_drone_comp/Screenshot_2023-06-04_at_2.54.49_PM.png" alt="Image 1" width="400" height="400" />
  <img src="circuit_drone_comp/Screenshot_2023-06-04_at_2.55.04_PM.png" alt="Image 2" width="400" height="400" />
</div>

