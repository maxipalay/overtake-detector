# quick workaround to import grandparent-directory
import sys
sys.path.append("...")
import global_vars
from time import sleep

def lines_detect_thread(image_ready, inference_done):
    # declare local variables, interpreter, etc
    # ...
    while True:
        print("lines_detect_thread waiting to execute...")
        image_ready.wait() # wait for image to be ready
        print("lines_detect_thread executing")
        print("lines detect_thread reads image "+str(global_vars.image))
        # run inference
        sleep(.6)
        print("lines_detect_thread finished")
        inference_done.wait()   # inference finished
