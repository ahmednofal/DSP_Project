import numpy as np
import datautils as util
# import steganography as steg
wav_file_decimal = "wav_file_decimal.txt"

freq, wave = util.load_wav_file("emb_file.wav")
decimal_file = open(wav_file_decimal, "w")
for decimal in wave:
    decimal_file.write(str(decimal)+'\n')


