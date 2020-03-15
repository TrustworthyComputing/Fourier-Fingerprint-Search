// How to run:
//
// openscad -o rotated.stl -D 'model="../stl_files/humanoid.stl"; degrees=[0,0,90]' ./plots/rotate_90.scad
//

model = "../stl_files/humanoid.stl";
degrees = [0, 0, 90];

rotate(degrees) import(file = model);
