# CAD to Audio [![License MIT][badge-license]](LICENSE)

## Signature Generation of STL files

1. Map vertices of STL triangles on a 3D plane. 
    * Scale objects to fit in a grid of a predefined size.
    
1. Use **FFT** to get frequencies and magnitudes.
    * We see frequencies and their magnitudes, but we don't know where in the design.
    
1. We need to know in which part of the design each frequency appeared.
    * Introduce sliding window (Split the design in **chunks**) w.r.t. X, Y, and Z axes.
    * Resulting slices can be used to perform **2D-FFT** (lower complexity but requires quantization), or **3D-FFT** (higher complexity and storage requirements but more accurate characterization of design). 

1. For each chunk we need to find which frequencies are the most important.
    * **Peaks**: Frequencies with the highest magnitude.
    * Number of retrieved peaks determined by adjustable threshold.
    
1. Within each chunk identify the frequencies with the highest magnitude.
    * This information forms a **signature** for this chunk of the design, and this signature becomes part of the fingerprint of the design as a whole.
    * Fingerprint: union of signatures for each chunk of the design. 

1. Use a **hash table** to make search fast.
    * The signatures become the key to our hash table.
    * Value is a tuple of (chunk_i, STL_ID). chunk_i identifies the chunk this frequency appeared in the STL_ID design.


## Installation
```
pip install -r requirements.txt
```


## STereoLithography (STL) Files 

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



## Visualize STL files with [OpenSCAD](https://www.openscad.org/):

```
import("absolute-path-to-repo/cad-to-audio/3d-models/boat-ascii.stl");
```


### ![alt text][twc-logo] An open-source project by Trustworthy Computing Group

[twc-logo]: ./logos/twc.png

[badge-license]: https://img.shields.io/badge/license-MIT-green.svg?style=flat-square
