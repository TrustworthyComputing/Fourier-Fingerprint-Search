/**
How to run:
* in the model specify the input STL file
* optionally provide a color in the col argument
* in the -o specify the output image name

openscad -o ./images/humanoid.png -D 'model="./stl_files/humanoid.stl"; col=[0, 0.55, 0.81]' --autocenter --viewall --colorscheme Nature --imgsize 3000,3000 ./open_stl.scad
*/

model = "/home/jimouris/Downloads/FabWave/CAD_1_15/Gasket/7bcbb8883-e1f4-4560-ae4d-9944e6a3f142-ascii.stl";
col = [0, 0.55, 0.81];
color(col) import(file = model);
