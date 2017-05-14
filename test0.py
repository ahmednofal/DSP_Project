import numpy as np
import steganography as steg
import datautils as utils
import os

def write_dec(vector, target):
    file = open(target, 'w')
    print(len(vector))
    for i in vector[0:len(vector) - 1]:
        file.write("%s\n" % str(i))
    file.write(str(vector[-1]))
    file.close()

def read_list(file):
    with open(file) as stream:
        data = stream.readlines()
    data = [x.strip() for x in data]
    return data

def stage0(source, target):
    freq, signal = utils.load_wav_file(source)
    write_dec(signal, target)
    return freq, signal

def stage1(cmd):
    os.system(cmd)

def stage2(bin_file):
    data = ""
    with open(bin_file) as stream:
        for line in stream:
            line = line.strip()
            data += line
    return data

def stage3(cover_file):
    cover = read_list(cover_file)
    return cover

def stage4(emb, cover):
    stego = steg.hide(cover, emb)
    return stego

def stage5(vector, file, bin_file, cmd):
    write_dec(vector, file)
    os.system(cmd)
    data = read_list(bin_file)
    return data

def stage6(length, data, file):
    data_recv = steg.recover(data, length)
    write_dec(data_recv,file)

PATH = os.getcwd() + '/'
cover = "cover_file"
emb = "emb_file"
stego = "stego"
recv = "recv"
cover_txt = cover + ".txt"
cover_wav = cover + ".wav"
cover_bin = cover + ".bin"
emb_txt = emb + ".txt"
emb_wav = emb + ".wav"
emb_bin = emb + ".bin"
stego_wav = stego + ".wav"
stego_txt = stego + ".txt"
stego_bin = stego + ".bin"
recv_wav = recv + ".wav"
recv_bin = recv + ".bin"
recv_txt = recv + ".txt"

# read wav file and dump values 
orig_f, orig_sig = stage0(cover_wav, cover_txt) 
emb_f, emb_sig = stage0(emb_wav, emb_txt)

# convert signal wav list to binary
cmd_l2b = PATH + "int_to_bin_out" + " " + cover_txt + " " + cover_bin
cmd_l2b_e = PATH + "int_to_bin_out" + " " + emb_txt + " " + emb_bin
stage1(cmd_l2b)
stage1(cmd_l2b_e)

# flatten emb msg
flat_emb = stage2(emb_bin)

# fetch orignal signal binary
orig_sig_b = stage3(cover_bin)

# hide emb msg in cover
stego = stage4(flat_emb, orig_sig)

# dump stego and convert to binary
cmd_l2b_s = PATH + "int_to_bin_out" + " " + stego_txt + " " + stego_bin
stego_bin = stage5(stego, stego_txt, stego_bin, cmd_l2b_s)
print(stego_bin)

# recover msg and dump recovered data
emb_len = len(flat_emb)
stage6(emb_len, stego_bin, recv_bin) 

# convert recoverd data to decimal
# ....

# read decimal and write to wav
# ....
