import numpy as np
import wave
from scipy.io.wavfile import read, write
import os
from pathlib import Path
from bitarray import *


reconstructed = '_reconstructed'
local_path = str(Path(os.getcwd()).parent)+'/'
recorded_wav_file = 'ahmednofal_8khz_32bitfloatPCM'
audio_file_format = '.wav'
path_for_recorded = local_path + 'WAV_Files/recorded/' + recorded_wav_file + audio_file_format
path_for_recorded_emb = ''
WAV_Files_folder = local_path + 'WAV_Files2/'
recorded_wav_folder = WAV_Files_folder + 'recorded/'
reconstructed_wav_folder = WAV_Files_folder  + 'reconstructed/'

reconstructed_wav_file = recorded_wav_file + reconstructed
save_figures_path = local_path + 'Figures2/'
real_part = save_figures_path + 'real_part'
imag_part = save_figures_path + 'imag_part'
phase_part = save_figures_path + 'phase_part'
magnitude_part = save_figures_path + 'magnitude_part'
discrete_signal_file_path = save_figures_path + 'discrete_signal'
reconstructed_signal_file_path = save_figures_path + 'reconstructed_signal_256'
file_format = '.pdf'
discrete_signal = 'Discrete Signal'

if not os.path.exists(save_figures_path):
    os.makedirs(save_figures_path)
if not os.path.exists(WAV_Files_folder):
    os.makedirs(WAV_Files_folder)
if not os.path.exists(reconstructed_wav_folder):
    os.makedirs(reconstructed_wav_folder)


# number of samples for the signal
samplesNum = 256
# DftPointsNum = 256
samplingRate = 2

def load_wav_file_as_bin(filename):
    sampleFrequency, inputSequence = read(filename)
    inputSequence = np.array(inputSequence)
    target = open('input_seq.txt', 'w')
    for i in inputSequence:
        target.write(str(i))

def load_wav_file(filename):

    sampleFrequency, inputSequence = read(filename)

    sampleFrequency = np.array(sampleFrequency)
    inputSequence = np.array(inputSequence)
    return sampleFrequency, inputSequence


def write_wav_file(filename, rate, data):
    write(filename=filename, rate=rate, data=data)


def hide_bit(target, bit, level): #hides <bit> in target number in bit number <level>
    if (int(bit) == 1):
        target = target | (bit << level)
    else:
        target = target & (~(1 << level))
    return target


def get_hidden_bit(source, level): #recovers a hidden bit in source number in bit number <level>
    return  (source >> level) & 1 


