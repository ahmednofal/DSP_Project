import numpy as np
import datautils as util
import steganography as steg

freq, wave = util.load_wav_file("karim3.wav")

print(freq)
print(wave.shape)
print(type(wave))
print(wave)
wave_bin = util.to_binary(wave, 32)

#print(wave_bin.shape)
