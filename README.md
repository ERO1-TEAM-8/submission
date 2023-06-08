# 1. Add permission to execute the script:
chmod +x main.sh
# 2. Run Drone Simulation:
./main.sh drone Sector,City,Country

# 3. Run Snow Removal Simulation:
./main.sh snowremoval Sector,City,Country

# Output
1. Open graphs plots
2. Close them
3. Generate GIF
4. Open the GIF and html graph , to play with ,  in the safari browser
# ⚠️ Warning
You need to have conda 4.13.0 installed and added to your path.

Works only on macos!

If u want to run it on another OS:

You need to check the path of conda.sh and replace it in the script where there is source command 

The lines to replace are located in the main.sh file at the root of the project:

line 48: source ~/opt/anaconda3/etc/profile.d/conda.sh

line 90: source ~/opt/anaconda3/etc/profile.d/conda.sh 

line 105 -> 129 : change safari with your appropriate browser

# Donate  🙏 and Have FUN 🤩
paypal.me/project_maintainer (JK)

# Snow Removal Circuit Simulation , Leynhac, France
![Alt Text](circuit_snow_removal/gif/cpp_route_animation.gif)


# Model Comparaison Drone , Outremont, Montreal, Canada , Hmmm... Why it Cost More ...?
<div >
  <img src="circuit_drone_comp/normal.png" alt="Image 1" width="400" height="400" />
  <img src="circuit_drone_comp/opti.png" alt="Image 2" width="400" height="400" />
</div>

# Model comparaison Drone Simulation, Leynhac, France


![Image 1](circuit_drone_comp/gif/circuit_drone.gif)
*Normal Circuit*

![Image 2](circuit_drone_comp/gif/circuit_drone2.gif)
*Opti circuit*


# For fun: Play with the graph


![Alt Text](circuit_drone_comp/anim1.png)

![Alt Text](circuit_drone_comp/anim2.png)

![Alt Text](circuit_drone_comp/anim3.png)

