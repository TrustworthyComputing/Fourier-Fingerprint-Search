translate([0,0,-20]) color([0, 0.55, 0.81]) import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

color([0.7, 0.7, 0.7 ,0.4])  {
   square(size = 70, center = true);
   rotate([0,45,0]) square(size = 70, center = true);
   rotate([0,90,0]) square(size = 70, center = true);
   rotate([0,135,0]) square(size = 70, center = true);
}


translate([100,0,-20]) color([0, 0.55, 0.81]) import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");
translate([100,0,0]) rotate([0,0,90]) color([0.7, 0.7, 0.7 ,0.4])  {
   square(size = 70, center = true);
   rotate([0,45,0]) square(size = 70, center = true);
   rotate([0,90,0]) square(size = 70, center = true);
   rotate([0,135,0]) square(size = 70, center = true);
}

translate([-100,0,-20]) color([0, 0.55, 0.81]) import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");
translate([-100,0,0]) rotate([90,0,0]) color([0.7, 0.7, 0.7 ,0.4])  {
   square(size = 70, center = true);
   rotate([0,45,0]) square(size = 70, center = true);
   rotate([0,90,0]) square(size = 70, center = true);
   rotate([0,135,0]) square(size = 70, center = true);
}
