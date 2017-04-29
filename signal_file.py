# directives

import numpy as np
from math import sqrt, atan
from enum import Enum
import numpy as np

# DFT implementation
""" * The implementation relies heavily on the numpy
    library to execute the summation of all of the sample
    entries in the samples array
"""

"""
    The DFT require implementing the sampling step first
    this step was included in the last assignment hence the code will be copied
"""
"""
    *   Several point will be chosen as our DFT samples and will be treated using the DFT
    The variable DftPointsNum will be the carrier of the number of the DftPointsNum
    *   There might be an inclusion of a feature to choose over which interval points should be extracted
"""


class Mode(Enum):
    NORMAL = 1
    INVERSE = 0


class signal__():
    def __init__(self):

        self.dft = None
        self.idft = None
        self.angle = None
        self.amplitude = None
        self.DftPointsNum = None
        self.samplingRate = None
        self.samplesNum = None
        self.x = None
        self.cos_arr = None
        self.sin_arr = None
        self.dft_real = None
        self.dft_imag = None
        self.frequencyAxis = None
        self.samplesIdx = None
        self.continuousSignal = None
        self.time_axis = None
        self.curr_exp_holder = None
        self.idft_magnitude_values = None
        self.__calculated_dft = False
        self.generated_signal = False

    # linspace(0, n, num=n / fs, endpoint=False)  #
    def GenerateSignal(self, n=50000, fs=1):
        self.samplesIdx = np.arange(n)
        self.continuousSignal = (
            (np.sin(2 * np.pi * self.samplesIdx / 40) + (2 * np.sin(2 * np.pi * self.samplesIdx / 16))) * np.exp(
                -((self.samplesIdx - 128) / 64) ** 2))
        self.samplesNum = int(n)
        self.samplingRate = float(fs)
        self.generated_signal = True
        return self.continuousSignal, self.samplesIdx

    def calculate_dft(self, samplingRate=2, DftPointsNum=256, samplesNum=300, mode=Mode.NORMAL):
        if not self.__calculated_dft and self.generated_signal:
            self.DftPointsNum = int(DftPointsNum)
            # defining the fundamental requency, will be used to define the spacing of the frequency axis
            fundamentalFrequency = self.samplingRate / self.DftPointsNum  # fs / N

            # Initialization

            self.dft = np.empty([self.DftPointsNum, ], dtype=complex)
            self.dft_real = np.empty([self.DftPointsNum, ])
            self.dft_imag = np.empty([self.DftPointsNum, ])
            self.cos_array = np.empty([self.DftPointsNum, ])
            self.sin_array = np.empty([self.DftPointsNum, ])

            self.frequencyAxis = fundamentalFrequency * np.arange(self.DftPointsNum)  # m * fs / N

            # getting the amplitude_values and samplesIdx for the generated signal


            # dft
            dft_range = np.arange(self.DftPointsNum)
            for m in range(self.DftPointsNum):
                self.cos_array = self.continuousSignal * np.cos(2 * np.pi * m * dft_range / self.DftPointsNum)
                self.sin_array = self.continuousSignal * np.sin(2 * np.pi * m * dft_range / self.DftPointsNum)
                self.dft_real[m] = np.sum(self.cos_array)
                self.dft_imag[m] = np.sum(self.sin_array)

            self.dft.imag = -self.dft_imag
            self.dft.real = self.dft_real
            self.__calculated_dft = True
            # sending back the dft aplitude values and the frequency components

            return self.dft, self.frequencyAxis
        else:
            if not mode.value and self.generated_signal:
                self.idft = np.empty([self.DftPointsNum, ], dtype=complex)
                dft_range = np.arange(self.DftPointsNum)
                for n in range(self.DftPointsNum):
                    self.idft[n] = np.sum(self.dft * (np.cos(2 * np.pi * n * dft_range / self.DftPointsNum) + np.sin(
                        2 * np.pi * n * dft_range / self.DftPointsNum) * 1j))
                self.idft /= self.DftPointsNum

                return self.idft
            else:
                pass

    def calculate_idft(self):

        if type(self.dft) is not None and self.generated_signal:
            self.calculate_dft(mode=Mode.INVERSE)
            self.time_axis = np.arange(self.DftPointsNum)
            self.to_polar(mode=Mode.INVERSE)
            return self.idft, self.time_axis

        else:
            pass

    def to_polar(self, mode=Mode.NORMAL):
        if self.__calculated_dft and mode.value and self.generated_signal:
            self.amplitude = np.empty([self.DftPointsNum, ])
            self.angle = np.empty([self.DftPointsNum, ])
            for m in range(self.DftPointsNum):
                self.amplitude[m] = sqrt(self.dft[m].real ** 2 + self.dft[m].imag ** 2)

            self.angle = np.angle(self.dft)
            return self.angle, self.amplitude
        else:
            if not mode.value and self.generated_signal:
                self.idft_magnitude_values = np.empty([self.DftPointsNum, ])
                for n in range(self.DftPointsNum):
                    self.idft_magnitude_values[n] = sqrt(self.idft[n].real ** 2 + self.idft[n].imag ** 2)
                return self.idft_magnitude_values
