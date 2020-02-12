# CAD to Audio [![License MIT][badge-license]](LICENSE)

## Shapes to Sound


#### 1. Basic shapes to arrays

##### Array Structure

* cube(3)
    | Index | Frequency	| Amplitude | Meaning        |
    |:-----:|:---------:|:---------:|:--------------:|
    |  0  	| 100  	    | cube_id   | Shape id       |
    |  1    | 200  	    | 1      	| # of fields    |
    |  2    | 300  	    | 3      	| field #1       |

* cube(4)
    | Index | Frequency	| Amplitude | Meaning        |
    |:-----:|:---------:|:---------:|:--------------:|
    |  3  	| 400  	    | cube_id   | Shape id       |
    |  4    | 500  	    | 1      	| # of fields    |
    |  5    | 600  	    | 4      	| field #1       |


#### 2. Arrays to sound

Make a sin wave for each (non-zero) element of the array. Play `k` of them for some agreed-upon interval of time (`t`). We can play multiple shapes at the same time (`k`). Then after `t` continue to the next `k` shapes. Both `t` and `k` are configurable.

##### Example
```
7 total shapes.
k = 5
t = 10 sec.

Play the first 5 sin waves that correspond to the 5 first shapes for 10 seconds. Continue with the remaining 2 for another 10 seconds. 
```




### STereoLithography (STL) Files 

The main purpose of the STL file format is to encode the surface geometry of a 3D object.

STL stores the following information:
* The coordinates of the vertices.
* The components of the unit normal vector to the triangle. The normal vector should point outwards with respect to the 3D model.


STL supports both binary and ASCII format. The binary format is always recommended for 3D printing since it results in smaller file sizes.

The ASCII files is in the following format:
```
solid OpenSCAD_Model
    facet normal 0 0 1
        outer loop
            vertex -15.829 0 55.75
            vertex -15.847 0.417 55.75
            vertex -20.75 0 55.75
        endloop
    endfacet
    facet normal 0 -0 1
        outer loop
        ...
        ...
        endloop
    endfacet
endsolid OpenSCAD_Model
```


### Compressing and decompressing STL files

To compress STL files by removing redundant strings and produce a compreesed STL (cstl) file:

```
python compress-stl.py --stl ./3d-models/boat-ascii.stl
```

To decompressing custom CSTL files to get back the original STL:
```
python decompress-stl.py --cstl ./3d-models/boat-ascii.cstl --out ./3d-models/boat-ascii-recovered.stl
```

Finally, to check the results:
```
diff ./3d-models/boat-ascii.stl ./3d-models/boat-ascii-recovered.stl
```


#### Visualize STL files with [OpenSCAD](https://www.openscad.org/):

```
import("absolute-path-to-repo/cad-to-audio/3d-models/boat-ascii.stl");
```


### ![alt text][twc-logo] An open-source project by Trustworthy Computing Group

[twc-logo]: ./logos/twc.png

[badge-license]: https://img.shields.io/badge/license-MIT-green.svg?style=flat-square
