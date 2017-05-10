import numpy as np
import datautils as util
import steganography as steg

freq, wave = util.load_wav_file("karim3.wav")

print(freq)
print(wave.shape)

wave_bin = util.array_to_binary(wave)

print(wave_bin.shape)
