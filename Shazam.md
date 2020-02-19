# Signature Generation of Songs

## Idea:

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

    
## Pseudocode:

```
'''
Generate the fingerprint of a STL file and store it in the hash table.
    ht          : Hash table quickly retrieve (slice index and STL file name) from signatures  
    stl_file    : STL input file name.
    num_slices  : Number of slices to split the STL file to.
    num_freqs   : Number of frequencies to split each slice to.
    amp_min     : Minimum amplitude in spectrogram in order to be considered a peak.
'''
def fingerprint(ht, stl_file, num_slices, num_freqs, amp_min):
    shapes = parse_stl(stl_file)
    
    shapes_freq = fft(shapes)

    # Split STL to slices/chunks
    slices = split_to_slices(shapes_freq, num_slices)       # configurable (e.g., 10)
    
    for slice_idx in range(len(slices)):
        slice = slices[slice_idx]
         
        # Split each slice to frequency intervals
        freqs = split_to_freq_intervals(slice, num_freqs)   # configurable (e.g., 4)
        
        # For each frequency interval find the peak
        peaks = []
        for freq in freqs:
            p = find_peak(freq)
            peaks.append(p)
        
        # Hash the peaks of this slice to get the signature
        signature = hash(peaks)
        
        ht.put(signature, (slice_idx, stl_file))
```



