# CAD to Audio [![License MIT][badge-license]](LICENSE)

## Signature Generation of Songs

1. Use **FFT** to get frequencies and magnitudes.
    * With FFT we lose information about timing.
    * We see frequencies and their magnitudes, but we don't know when in the song they appeared.
    
1. We need to know at what point of time each frequency appeared.
    * Introduce sliding window (Split the song in **chunks**).

1. For each chunk we need to find which frequencies are the most important.
    * **Peaks**: Frequencies with the highest magnitude.

1. We have a wide range of frequencies.
    * Use **frequency intervals** (e.g., freq-range/4).
    
1. Within each interval identify the frequency with the highest magnitude.
    * This information forms a **signature** for this chunk of the song, and this signature becomes part of the fingerprint of the song as a whole.
    * Fingerprint: union of signatures for each chunk of the song. 

1. Use a **hash table** to make search fast.
    * The signatures become the key to our hash table.
    * Value is a tuple of the times this frequencies appeared in each song along with the SongID.
    * Value is a tuple of (chunk_i, song_ID). chunk_i is the time this frequency appeared in the SongID song.



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
