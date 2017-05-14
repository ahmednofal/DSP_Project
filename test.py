import numpy as np
import matplotlib.pyplot as plt
import datautils as util
import os

import steganography as steg

def read_list(file):
    with open(file) as stream:
        data = stream.readlines()
    data = [int(x.strip()) for x in data]
    return data

def myPlot(y, x, t, xt, yt, b):
    if(b):
        plt.bar(x, y, width = 0, edgecolor = "k")
    else:
        plt.plot(x, y)
    plt.title(t)
    plt.xlabel(xt)
    plt.ylabel(yt)
    plt.savefig(t) #change 128 to 256
    plt.show()

def dft(N, x_n):
    M = np.arange(0, N, 1)
    x_m = []
    for n in M:
        coeff = np.pi * 2 * n / N 
        w = np.cos(coeff * M) - np.sin(coeff * M) * 1j #is w np array? -yes
        x_w = x_n * w #is x_w np array? -yes
        x_m.append(sum(x_w))
        if ((n / N * 100) % 1 < 0.01):
            print((n / N * 100), "% done")
    return x_m

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
# First let's dump it into a file for c++ code int_to_bin_conv.cpp
emb_file_decimal = open(emb_file_decimal_path, "w")
print(cover, "cover")
print(emb, "emb")
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
print(stego, "stego")

print("\n\n\twriting stego to decimal file\n\n")
stego_file_decimal = open(stego_file_decimal_path, "w+")
for value in stego:
    stego_file_decimal.write(str(value)+'\n')
#stego_file_decimal.write(str(stego))
stego_file_decimal.close()
print("\n\n\t\tconverting stego to bin\n\n")
os.system(convert_stego_to_binary)
print("done")



with open(stego_file_binary_path) as stego_file_binary :
    stego_file_binary_content = stego_file_binary.readlines()
stego = [x.strip() for x in stego_file_binary_content]


emb_message_recovered = steg.recover(stego, len(emb))
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
recovered_emb = np.asarray(recovered_emb, np.int16)
print(recovered_emb, "rec")
# print(type(recovered_emb[0]))
# print(recovered_emb[0])
util.write_wav_file(recovered_emb_file_name, emb_freq, recovered_emb)
print("done")

# write stego wav file
stego_data = read_list(stego_file_decimal_path) 
stego_data = np.asarray(stego_data, np.int16)
util.write_wav_file(local_path + "stego.wav", cover_freq, stego_data)

emb_freq, emb = util.load_wav_file(emb_file_name)

# analysis fft on signals
############# print(cover, stego) both have the same exact values somehow
cover_freq, cover = util.load_wav_file(cover_file_name)
cover_fft = np.fft.rfft(cover)
emb_fft = np.fft.rfft(emb)
stego_fft = np.fft.rfft(stego_data)

cover_bin = np.arange(len(cover)) * cover_freq / len(cover)
emb_bin = np.arange(len(emb)) * emb_freq / len(emb)

myPlot((cover - stego_data), np.arange(len(cover)) / cover_freq, "Difference(Cover-Mod)", "time(s)", "amplitude", 0)
myPlot(cover, np.arange(len(cover)) / cover_freq, "Cover_Signal", "time(s)", "amplitude", 0)
myPlot(stego_data, np.arange(len(cover)) / cover_freq, "Stgeo_signal", "time(s)", "amplitude", 0)
myPlot(emb, np.arange(len(emb)) / emb_freq, "Emb_signal", "time(s)", "amplitude", 0)
"""
cover_bin = cover_bin[0 : len(cover_fft)]
emb_bin = emb_bin[0 : len(emb_fft)]
cover_fft = [x.real for x in cover_fft]

diff_fft = cover_fft - stego_fft

myPlot(cover_fft, cover_bin, "Cover_fft", "freq(hz)", "amplitude", 0)
myPlot(emb_fft, emb_bin, "Embbeded_fft", "freq(hz)", "amplitude", 0)
myPlot(stego_fft, cover_bin, "Stego_fft", "freq(hz)", "amplitude", 0)
myPlot(diff_fft, cover_bin, "Diff_fft", "freq(hz)", "amplitude", 0)
# test
"""
