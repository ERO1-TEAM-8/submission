# Add permission to execute the script
chmod +x main.sh
# Run Drone Simulation 
./main.sh drone Sector,City,Country

# Run Snow Removal Simulation
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



<style>
  figure {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  figcaption {
    margin-bottom: 10px;
    text-align: center;
  }
</style>

<div>
  <figure>
    <figcaption>Normal Circuit</figcaption>
    <img src="circuit_drone_comp/gif/circuit_drone.gif" alt="Image 1" width="300" height="300" />
  </figure>
  <figure>
    <figcaption>Opti circuit</figcaption>
    <img src="circuit_drone_comp/gif/circuit_drone2.gif" alt="Image 2" width="300" height="300" />
  </figure>
</div>

