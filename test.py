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
# if not os.path.exists(emb_file_decimal_path):
#     os.makedirs(emb_file_decimal_path)
# if not os.path.exists(emb_file_binary_path):
#     os.makedirs(emb_file_binary_path)
# if not os.path.exists(stego_file_decimal_path):
#     os.makedirs(stego_file_decimal_path)
# if not os.path.exists(stego_file_binary_path):
#     os.makedirs(stego_file_binary_path)
# if not os.path.exists(recovered_emb_file_binary_path):
#     os.makedirs(recovered_emb_file_binary_path)
# if not os.path.exists(emb_file_decimal_path):
#     os.makedirs(recovered_emb_file_decimal_path)

convert_emb_to_binary = int_to_bin_out_exe + ' ' + emb_file_decimal_path \
                        + ' ' + emb_file_binary_path
convert_stego_to_binary = int_to_bin_out_exe + ' ' + stego_file_decimal_path \
                          + ' ' + stego_file_binary_path
convert_recovered_emb_to_decimal = bin_to_int_out_exe + ' ' + recovered_emb_file_binary_path \
                                   + ' ' + recovered_emb_file_decimal_path

emb_freq, emb = util.load_wav_file(emb_file_name)
cover_freq, cover = util.load_wav_file(cover_file_name)
print(type(cover[0]))
# First let's dump it into a file for c++ code int_to_bin_conv.cpp
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

stego = steg.hide(cover, emb)

print("\n\n\twriting stego to decimal file\n\n")
stego_file_decimal = open(stego_file_decimal_path, "w+")
for value in stego:
    stego_file_decimal.write(str(value)+'\n')
print("done")
#stego_file_decimal.write(str(stego))
stego_file_decimal.close()
print("\n\n\t\tconverting stego to bin\n\n")
os.system(convert_stego_to_binary)
print("done")



with open(stego_file_binary_path) as stego_file_binary :
    stego_file_binary_content = stego_file_binary.readlines()
stego = [x.strip() for x in stego_file_binary_content]

emb_message_recovered = steg.recover(stego, len(emb))
print("done")
#print(emb_message_recovered)
with open(recovered_emb_file_binary_path, "w+") as recovered_emb_file_binary:
    for binary in emb_message_recovered[0:len(emb_message_recovered) - 1]:
        recovered_emb_file_binary.write(str(binary)+'\n')

os.system(convert_recovered_emb_to_decimal)
print("done")

with open(recovered_emb_file_decimal_path, "r") as recovered_emb_file_decimal:
    recovered_emb_file_decimal_content = recovered_emb_file_decimal.readlines()
recovered_emb = np.array([x.strip() for x in recovered_emb_file_decimal_content])
print("done")

util.write_wav_file(recovered_emb_file_name, emb_freq, recovered_emb)
print("done")
