# This files contains the implementation of the Steganography effect using Phase coding
# The source for the theory of the implementation will be in the external sources file.
# What TO DO :
# According to the source:

# 1- Get audio file( supposed to be created using the audio morphing techniques)
# 2- Convert audio file into continuous line of bits ( For LSB Coding)- also the audio will be typically amplified to
# always account for the deterioration of the signal due to the LSB
# 3- Convert the audio file into the frequency domain for it to be processed using the spread spectrum technique
# 4- All audio files will be of mono type

from datautils import *
from enum import Enum

# Global constant to be used by all functions for sync purposes

quantization_bit_value = 16


# The lsb_code function is to implement the lsb coding technique for steganography, papers file include papers
# explaining the theory behind the standard and the implementation
# The function needs one input and produces one output
# The inputs will be the message to be embedded
# The output will be the rate and the amplitude values
# There might be modification to the function in terms of the number of bits used to represent the signal whether it is
# only one bit of more of the original amplitude
# To use the LSB steganography approach u should use high amplitude signals, amplify low signals or record with high amp
# from the start
# Another parameter that could be added would be the factor by which the amplitude will be amplified


class Method(Enum):
    lsb_coding = 0
    phase_coding = 1


def hide(cover_audio_file, emb_audio_file, method=Method.lsb_coding):
    binary_cover_message_rate, binary_cover_message = load_wav_file_in_binary(cover_audio_file)

    # We have the covering audio file amps in binary format
    # We need to convert the embedded file into binary as well
    binary_emb_message_rate, binary_emb_message = load_wav_file_in_binary(emb_audio_file)
    if method == Method.lsb_coding:
        binary_emb_message = to_binary(binary_emb_message)
        lsb_code(binary_emb_message, binary_cover_message)


def lsb_code(binary_emb_message, binary_cover_message):
    # Binary manipulation
    # The LSB of each array entry in the amplitude array of the cover signal will be switched to comply with the ith
    # bit in the embedded signal (the mask_lsb function)
    # A suggested scheme would be to require that the cover audio be big enough (in time) to contain the embedded signal
    # For the library to be usable the first scheme is used with a warning raised for the user to enter a taller(in time
    # length) cover audio

    lsb_chooser_array = len(binary_emb_message) / binary_cover_message.shape[0]

    emb_message_bits_length = len(binary_emb_message)

    lsb_idx = 0
    # Loop over all the bits in the binary_emb_message
    for k in range(emb_message_bits_length):
        if (float(k) / float(binary_cover_message.shape[0])) > 1:
            lsb_idx += 1
        binary_cover_message[k] = hide_bit(binary_emb_message[k],
                                           binary_cover_message[k % binary_cover_message.shape[0]],
                                           lsb_idx)


def hide_bit(bit, word, bit_to_be_replaced_idx):
    bit_to_be_replaced_value = mask_bit(bit_to_be_replaced_idx, word)
    if bit:
        if not bit_to_be_replaced_value:  # The bit to be replaced is zero and the bit to be hidden is one so we add the
            # the value of that bit in decimal to the value of the word
            word = word + 2 ** bit_to_be_replaced_idx
    else:
        if bit_to_be_replaced_value:
            word = word - 2 ** bit_to_be_replaced_idx
    return word


def mask_bit(idx, message):
    masker = message & (1 << idx)
    masker = masker >> idx
    return masker


def recover(cover_audio_file):
    # Take the cover audio file and reverse the hiding process by taking the lsb bit and adding it to an array of bits
    # One challenge is due to our algorithm of hiding the lsb, because we do not know how many bits (in the amp values
    # of the original cover message was used to hide the emb message binary code
    pass