import multiprocessing as mp
import threading as th
from queue import Queue

from datetime import date
import time
from cv.lanes.lanes_detection import lines_detect
from cv.signs.signs_detection import signs_detect
import cv2
import numpy as np
import global_vars
global_vars.init()
from gps.GPSmodule import GPS
from comms.check_connection import check_connection 
import config as cfg
cfg.init()
from cv.camera import Camera
from time import sleep
from comms.data_saver import save_infraction
from comms.upload_data import upload_data

# sychronization mechanisms for processes 
image_ready = mp.Barrier(3)       # barrier that holds inference until data is ready
inference_done = mp.Barrier(3)   # barrier that holds main until inference on both networks is done
conn_queue = Queue(maxsize=1)

process_lanes = mp.Process(name="lanes_detect", target=lines_detect, daemon=True, args=(image_ready, inference_done,))
process_signs = mp.Process(name="signs_detect", target=signs_detect, daemon=True, args=(image_ready, inference_done,))
process_lanes.start()
process_signs.start()

thread_check_conn = th.Thread(name="check_connection", target=check_connection, daemon=True, args=(conn_queue,))
thread_check_conn.start()

def main():
    prev_frame_overtaking = False
    was_overtaking = False
    camera = Camera()
    gps = GPS()
    internet_connection = False
    while (True):
        # check for internet connection
        if not conn_queue.empty():
            conn=conn_queue.get_nowait()
            internet_connection = conn
        
        if internet_connection:
            # send data to server
            upload_data()
            sleep(10)
        
        else:
            start = time.time()
            # get camera frame
            frame = camera.get_frame()
            if frame is None:
                break
            
            # set shared variable
            global_vars.image[:]=frame.reshape(224*224*3)
        
            # show image (debugging)
            cv2.imshow('input',cv2.cvtColor(np.frombuffer(global_vars.image).reshape(224,224,3).astype(np.uint8),cv2.COLOR_RGB2BGR))
            cv2.waitKey(1) & 0xFF

            # release inference processes
            image_ready.wait()

            # while waiting for BOTH inference threads to complete, lets read gps data and current time
            gps_data = gps.get_gps_data()

            current_time = time.time()
            
            # wait for inference completion
            inference_done.wait() # wait for inferences to complete
            
            # print raw results from lines inference (debugging)
            print("time: {:4f} | can overtake: {} | overtaking: {}".format(time.time()-start,global_vars.can_overtake_lanes.value, global_vars.overtaking.value))
        
            # aplicamos un "LPF", consideramos que estamos pasando solo si en los ultimos dos cuadros la red dijo que estabamos pasando
            overtaking = prev_frame_overtaking and global_vars.overtaking
            
            # check if an infraction is taking place
            if overtaking and not was_overtaking and (not global_vars.can_overtake_lanes or not global_vars.can_overtake_signs):
                print("OVERTAKING, saving data")
                dat = date.fromtimestamp(current_time)
                save_infraction(frame, dat.strftime("%Y%m%d"),dat.strftime("%H%M%S"), gps_data)
            # update filter variables
            prev_frame_overtaking = global_vars.overtaking  # retain previous value of global_vars.overtaking
            was_overtaking = overtaking                     # retain value of overtaking

main()

'''
send_data_thread()  # checks for wifi connection, if it finds one it will try to send recorded data
lines_detect_thread() # road lines detection
signs_detect_thread() # signs detection
alerts_thread()
gps_logger_thread()
'''
