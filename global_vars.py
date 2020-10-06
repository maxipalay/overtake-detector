import multiprocessing as mp
import ctypes
import numpy as np
def init():
    global image
    global can_overtake_signs
    global can_overtake_lanes
    global overtaking

    can_overtake_lanes = mp.RawValue(ctypes.c_bool)
    can_overtake_signs = mp.RawValue(ctypes.c_bool)
    overtaking = mp.RawValue(ctypes.c_bool)
    image = mp.RawArray(ctypes.c_double, 224*224*3) # allocate shared memory    
