/**
How to run:
* in the model specify the input STL file
* optionally provide a color in the col argument
* in the -o specify the output image name

openscad -o ./images/humanoid.png -D 'model="./stl_files/humanoid.stl"; col=[0, 0.55, 0.81]' --autocenter --viewall --colorscheme Nature --imgsize 3000,3000 ./open_stl.scad
*/

model = "./stl_files/humanoid.stl";
col = [0.7, 0.7, 0.7, 0.4];

color(col) import(file = model);
