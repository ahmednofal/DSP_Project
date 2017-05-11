import numpy as np
import datautils as util
import steganography as steg

freq, wave = util.load_wav_file("karim3.wav")
print(type(wave[0]))
print(wave.shape[0])
print(wave)
#print(freq)
#print(wave.shape)
#print(type(wave))
wave_bin = util.to_binary(wave)
print(wave_bin)
wave_bin += 'ahmed'
print(wave_bin[-5:])
print(len(wave_bin))
#print(wave_bin.shape)
