color([0, 0.55, 0.81]) import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

color([0.7, 0.7, 0.7 ,0.4])  {
    square(size = 70, center = true);
    translate([0,0,24]) square(size = 70, center = true);
    translate([0,0,48]) square(size = 70, center = true);
}

translate([100,0,0]) {
    color([0, 0.55, 0.81])
    import("/home/jimouris/Downloads/3d_models/boat.stl");

    color([0.7, 0.7, 0.7 ,0.4])  {
        rotate([90,0,0]) translate([0,20,-18]) {
            square(size = 70, center = true);
            translate([0,0,18]) square(size = 70, center = true);
            translate([0,0,36]) square(size = 70, center = true);
        }
    }
}

translate([-100,0,0]) {
    color([0, 0.55, 0.81])
    import("/home/jimouris/Downloads/3d_models/boat.stl");

    color([0.7, 0.7, 0.7 ,0.4])  {
        rotate([0,90,0]) translate([-20,0,-30]) {
            square(size = 70, center = true);
            translate([0,0,31]) square(size = 70, center = true);
            translate([0,0,62]) square(size = 70, center = true);
        }
    }
}