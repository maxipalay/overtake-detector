# quick workaround to import from grantparent-directory
import sys
sys.path.append("...")
import global_vars
import numpy as np

def signs_detect(image_ready, inference_done):
    
    # declarations and one-time things

    while True:
        #print("signs_detect_thread waiting to execute...") #debug
        image_ready.wait() # wait for image to be ready
        #print("signs_detect_thread executing")  #debug
        frame_input = np.frombuffer(global_vars.image).reshape(224,224,3)
        #execute inference
        #print("signs_detect_thread finished")   #debug
        inference_done.wait()   # inference finished
