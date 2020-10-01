# quick workaround to import from grantparent-directory
import sys
sys.path.append("...")
import global_vars
from time import sleep
def signs_detect_thread(image_ready, inference_done):
    
    # declarations and one-time things

    while True:
        print("signs_detect_thread waiting to execute...")
        image_ready.wait() # wait for image to be ready
        print("signs_detect_thread executing")
        #execute inference
        sleep(.4)
        print("signs_detect_thread reads image "+str(global_vars.image))
        print("signs_detect_thread finished")
        inference_done.wait()   # inference finished
