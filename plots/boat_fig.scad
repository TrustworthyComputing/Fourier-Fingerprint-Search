color([0, 0.55, 0.81]) import("/home/jimouris/Downloads/3d_models/boat.stl");


// rotate(a = 30) square(size = 100, center = true);

color([0.6, 0.6, 0.6 ,0.4])  {
    square(size = 80, center = true);
    translate([0,0,24]) square(size = 80, center = true);
    translate([0,0,48]) square(size = 80, center = true);
}


translate([100,0,0]) {
    color([0, 0.55, 0.81])
    import("/home/jimouris/Downloads/3d_models/boat.stl");

    color([0.6, 0.6, 0.6 ,0.4])  {
        rotate([0,90,0]) translate([-20,0,-30]) {
            square(size = 80, center = true);
            translate([0,0,31]) square(size = 80, center = true);
            translate([0,0,62]) square(size = 80, center = true);
        }
    }
}

translate([-100,0,0]) {
    color([0, 0.55, 0.81])
    import("/home/jimouris/Downloads/3d_models/boat.stl");

    color([0.6, 0.6, 0.6 ,0.4])  {
        rotate([90,0,0]) translate([0,20,-0]) {
            square(size = 80, center = true);
//            translate([0,0,31]) square(size = 80, center = true);
//            translate([0,0,62]) square(size = 80, center = true);
        }
    }
}