// How to run:
//
// openscad -o ./stl_files/rotated.stl -D 'model="./stl_files/humanoid.stl"; degrees=[0,0,90]' ./plots/rotate.scad
//

model = "./stl_files/humanoid.stl";
degrees = [0, 0, 90];

rotate(degrees) import(file = model);
