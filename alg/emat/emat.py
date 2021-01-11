import os

from ctypes import *



maxSize = 6144

class WaveData(Structure):
    _fields_ = [
        ("data", c_int32*maxSize),
    ]

def calThickness(data, gain_db, version, pluse_num=2, nSize=2048, vel_mps=3240, freq_Hz=40e6):

    ETGminiX1_file = os.path.dirname(os.path.abspath(__file__)) + '/thicknessgauge_x86_64_%s.so' % (version)
    # ETGminiX1_file = os.path.dirname(os.path.abspath(__file__)) + '/thicknessgauge_armv7l_%s.so' % (version)
    ETGminiX1 = CDLL(ETGminiX1_file)

    thick_mm = -19.0

    if (nSize<=maxSize):
        wdata = WaveData()
        for i in range(0, nSize):
            wdata.data[i] = data[i]
        # double MeasureEchoPosition(int32_t* SignalIn, int PulseNum, int GaindB)
        ETGminiX1.MeasureEchoPosition.argtypes = [c_void_p, c_int, c_int, c_int]
        ETGminiX1.MeasureEchoPosition.restype = c_double
        ret = ETGminiX1.MeasureEchoPosition(byref(wdata.data), pluse_num, gain_db, nSize)
        thick_mm = round(ret*vel_mps/freq_Hz/2*1000, 3)

    return thick_mm