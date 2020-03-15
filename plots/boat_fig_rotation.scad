translate([-120,0,0]) {
   color([0, 0.55, 0.81]) import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

   color([0.7, 0.7, 0.7 ,0.4])  {
       square(size = 70, center = true);
       translate([0,0,24]) square(size = 70, center = true);
       translate([0,0,48]) square(size = 70, center = true);
   }
}

translate([-40,0,0]) {
   rotate(a=45) color([0, 0.55, 0.81]) import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

   color([0.7, 0.7, 0.7 ,0.4])  {
       square(size = 70, center = true);
       translate([0,0,24]) square(size = 70, center = true);
       translate([0,0,48]) square(size = 70, center = true);
   }
}

translate([40,0,0]) {
   rotate(a=90) color([0, 0.55, 0.81]) import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

   color([0.7, 0.7, 0.7 ,0.4])  {
       square(size = 70, center = true);
       translate([0,0,24]) square(size = 70, center = true);
       translate([0,0,48]) square(size = 70, center = true);
   }
}

translate([120,0,0]) {
   rotate(a=135) color([0, 0.55, 0.81]) import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

   color([0.7, 0.7, 0.7 ,0.4])  {
       square(size = 70, center = true);
       translate([0,0,24]) square(size = 70, center = true);
       translate([0,0,48]) square(size = 70, center = true);
   }
}

//////////////////////////////////////////////////////////////////////////////

// Above
translate([-120,0,80]) {
    rotate([0,0,0]) 
    color([0, 0.55, 0.81])
    import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

    color([0.7, 0.7, 0.7 ,0.4])  {
        rotate([0,90,0]) translate([-20,0,-30]) {
            square(size = 70, center = true);
            translate([0,0,31]) square(size = 70, center = true);
            translate([0,0,62]) square(size = 70, center = true);
        }
    }
}

translate([-40,0,80]) {
    rotate([45,0,0]) 
    translate([0,15,-10])
    color([0, 0.55, 0.81])
    import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

    color([0.7, 0.7, 0.7 ,0.4])  {
        rotate([0,90,0]) translate([-20,0,-30]) {
            square(size = 70, center = true);
            translate([0,0,31]) square(size = 70, center = true);
            translate([0,0,62]) square(size = 70, center = true);
        }
    }
}

translate([40,0,80]) {
    rotate([90,0,0]) 
    translate([0,20,-20])
    color([0, 0.55, 0.81])
    import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

    color([0.7, 0.7, 0.7 ,0.4])  {
        rotate([0,90,0]) translate([-20,0,-30]) {
            square(size = 70, center = true);
            translate([0,0,31]) square(size = 70, center = true);
            translate([0,0,62]) square(size = 70, center = true);
        }
    }
}

translate([120,0,80]) {
    rotate([135,0,0]) 
    translate([0,15,-35])
    color([0, 0.55, 0.81])
    import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

    color([0.7, 0.7, 0.7 ,0.4])  {
        rotate([0,90,0]) translate([-20,0,-30]) {
            square(size = 70, center = true);
            translate([0,0,31]) square(size = 70, center = true);
            translate([0,0,62]) square(size = 70, center = true);
        }
    }
}

//////////////////////////////////////////////////////////////////////////////
 
// Below
translate([-120,0,-80]) {
   color([0, 0.55, 0.81])
   import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

   color([0.7, 0.7, 0.7 ,0.4])  {
       rotate([90,0,0]) translate([0,20,-18]) {
           square(size = 70, center = true);
           translate([0,0,18]) square(size = 70, center = true);
           translate([0,0,36]) square(size = 70, center = true);
       }
   }
}

translate([-40,0,-80]) {
   rotate([0,45,0]) 
   translate([-12,0,-5])
   color([0, 0.55, 0.81])
   import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

   color([0.7, 0.7, 0.7 ,0.4])  {
       rotate([90,0,0]) translate([0,20,-18]) {
           square(size = 70, center = true);
           translate([0,0,18]) square(size = 70, center = true);
           translate([0,0,36]) square(size = 70, center = true);
       }
   }
}

translate([40,0,-80]) {
   rotate([0,90,0]) 
   translate([-20,0,-20])
   color([0, 0.55, 0.81])
   import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

   color([0.7, 0.7, 0.7 ,0.4])  {
       rotate([90,0,0]) translate([0,20,-18]) {
           square(size = 70, center = true);
           translate([0,0,18]) square(size = 70, center = true);
           translate([0,0,36]) square(size = 70, center = true);
       }
   }
}

translate([120,0,-80]) {
   rotate([0,135,0]) 
   translate([-15,0,-30])
   color([0, 0.55, 0.81])
   import("/home/jimouris/repos/cad-to-audio/stl_files/boat.stl");

   color([0.7, 0.7, 0.7 ,0.4])  {
       rotate([90,0,0]) translate([0,20,-18]) {
           square(size = 70, center = true);
           translate([0,0,18]) square(size = 70, center = true);
           translate([0,0,36]) square(size = 70, center = true);
       }
   }
}