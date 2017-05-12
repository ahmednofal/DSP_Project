import numpy as np
import datautils as util
import os

import steganography as steg
local_path = os.getcwd()+'/'
int_to_bin_out_exe = local_path + 'int_to_bin_out'
bin_to_int_out_exe = local_path + 'bin_to_int_out'

wav_file_decimal = "wav_file_decimal.txt"
cover_file_name = "cover_file.wav"
emb_file_name = "emb_file.wav"
recovered_emb_file_name = "recovered_emb.wav"
emb_file_decimal_path = local_path + "emb_file_decimal.txt"
emb_file_binary_path = local_path + "emb_file_binary.txt"
stego_file_decimal_path = local_path + "stego_file_decimal.txt"
stego_file_binary_path = local_path + "stego_file_binary.txt"
recovered_emb_file_binary_path = local_path + "recovered_emb_file_binary.txt"
recovered_emb_file_decimal_path = local_path + "recovered_emb_file_decimal.txt"

convert_emb_to_binary = int_to_bin_out_exe + ' ' + emb_file_decimal_path \
                        + ' ' + emb_file_binary_path
convert_stego_to_binary = int_to_bin_out_exe + ' ' + stego_file_decimal_path \
                          + ' ' + stego_file_binary_path
convert_recovered_emb_to_decimal = bin_to_int_out_exe + ' ' + recovered_emb_file_binary_path \
                                   + ' ' + recovered_emb_file_decimal_path

print('l0')
emb_freq, emb = util.load_wav_file(emb_file_name)
print(emb)
print(type(emb[0]))
print('l1')
cover_freq, cover = util.load_wav_file(cover_file_name)
print(type(cover[0]))
print('l2')
# First let's dump it into a file for c++ code int_to_bin_conv.cpp
# print(emb)
emb_file_decimal = open(emb_file_decimal_path, "w")
for decimal in emb[0:len(emb) - 1]:
    emb_file_decimal.write(str(decimal)+'\n')

emb_file_decimal.write(str(decimal))
emb_file_decimal.close()

# To convert it to binary and store it for us as binary
os.system(convert_emb_to_binary)
emb = ''
with open(emb_file_binary_path, 'r') as emb_binary_file:
    for line in emb_binary_file:
        emb += line[:len(line)-1]
#print(emb)
print(cover)
stego = steg.hide(cover, emb)

stego_file_decimal = open(stego_file_decimal_path, "w")
for decimal in emb[0:len(emb) -1]:
    stego_file_decimal.write(str(stego)+'\n')

stego_file_decimal.write(str(stego))
stego_file_decimal.close()

os.system(convert_stego_to_binary)



with open(stego_file_binary_path) as stego_file_binary :
    stego_file_binary_content = stego_file_binary.readlines()
stego = [x.strip() for x in stego_file_binary_content]

emb_message_recovered = steg.recover(stego, len(emb))

os.system(convert_recovered_emb_to_decimal)

with open(recovered_emb_file_decimal_path) as recovered_emb_file_decimal:
    recovered_emb_file_decimal_content = recovered_emb_file_decimal.readlines()
recovered_emb = [x.strip() for x in recovered_emb_file_decimal_content]

util.write_wav_file(recovered_emb_file_name, emb_freq, recovered_emb)
