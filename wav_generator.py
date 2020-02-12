#!/usr/bin/python
# based on : www.daniweb.com/code/snippet263775.html
import math
import wave
import struct
import sys

# Audio will contain a long list of samples (i.e. floating point numbers describing the
# waveform).  If you were working with a very long sound you'd want to stream this to
# disk instead of buffering it all in memory list this.  But most sounds will fit in
# memory.
audio = []
sample_rate = 44100.0
freq_gap = 100

def stl_arr_to_wav():

    global audio

    arrayFileName = input("Enter the filename of the 1-D STL array: ")

    # read file (should be 1 line) of float values separated by commas
    with open(arrayFileName, 'r') as f:
        cad_array = f.read().split(',')

    # frequency encoded as freq_gap (144 Hz by default) * index
    # generates sinewave for 100 ms with volume equal to value of array index
    i = 0
    for element in cad_array:
        if element != 0.0:
            frequency = freq_gap * (i + 1)
            append_sinewave(frequency, 100, float(element))

    outputFileName = input("Enter a filename for WAV data (.wav): ")
    save_wav(outputFileName)

def append_sinewave(
        freq=440.0,
        duration_milliseconds=1000,
        volume=1.0):

    global audio

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):

        # 2*pi*f is just the angular frequency (https://en.wikipedia.org/wiki/Angular_frequency)
        # x / sample_rate just takes samples (snapshots) of the sinusoid
        # audio_samples = amplitude * sin(angular frequency * samples/sample_rate)
        # values should be normalized between 0 (no sound) to 1 (max volume)
        audio.append(volume * math.sin(2 * math.pi * freq * ( float(x) / sample_rate )) / 32767.0)

    return

def save_wav(file_name):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return

stl_arr_to_wav()
