# 1. Add permission to execute the script:
chmod +x main.sh
# 2. Run Drone Simulation:
./main.sh drone Sector,City,Country

# 3. Run Snow Removal Simulation:
./main.sh snow_removal Sector,City,Country

# ⚠️ Warning
You need to have conda 4.13.0 installed and added to your path.

Works only on macos!

If u want to run it on another OS:

You need to check the path of conda.sh and replace it in the script where there is source command 

The lines to replace are located in the main.sh file at the root of the project:

line 27: source ~/opt/anaconda3/etc/profile.d/conda.sh

line 74: source ~/opt/anaconda3/etc/profile.d/conda.sh 

# Donate  🙏 and Have FUN 🤩
paypal.me/project_maintainer (JK)

# Snow Removal Circuit Simulation , Leynhac, France
![Alt Text](circuit_snow_removal/gif/cpp_route_animation.gif)


# Model Comparaison Drone , Outremont, Montreal, Canada , Hmmm... Why it Cost More ...?
<div >
  <img src="circuit_drone_comp/Screenshot 2023-06-04 at 4.58.25 PM.png" alt="Image 1" width="400" height="400" />
  <img src="circuit_drone_comp/Screenshot 2023-06-04 at 4.58.31 PM.png" alt="Image 2" width="400" height="400" />
</div>

# Model comparaison Drone Simulation, Leynhac, France


![Image 1](circuit_drone_comp/gif/circuit_drone.gif)
*Normal Circuit*

![Image 2](circuit_drone_comp/gif/circuit_drone2.gif)
*Opti circuit*


# For fun: Play with the graph


![Alt Text](circuit_drone_comp/anim1.png)

