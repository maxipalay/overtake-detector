import multiprocessing as mp
import threading as th
from queue import Queue
from infraction import Infraction
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
from alerts.alerts import alert

# sychronization mechanisms for processes 
image_ready = mp.Barrier(3)       # barrier that holds inference until data is ready
inference_done = mp.Barrier(3)   # barrier that holds main until inference on both networks is done
conn_queue = Queue(maxsize=1)
alert_event = th.Event()

process_lanes = mp.Process(name="lanes_detect", target=lines_detect, daemon=True, args=(image_ready, inference_done,))
process_signs = mp.Process(name="signs_detect", target=signs_detect, daemon=True, args=(image_ready, inference_done,))
process_lanes.start()
process_signs.start()

thread_alerts = th.Thread(name="alerts_thread", target = alert, daemon=True, args=(alert_event,))
thread_alerts.start()
thread_check_conn = th.Thread(name="check_connection", target=check_connection, daemon=True, args=(conn_queue,))
thread_check_conn.start()

def main():
    overtaking = [False,False,False]
    prev_frame_overtaking = False
    was_overtaking = False
    camera = Camera()
    gps = GPS()
    internet_connection = False
    sleep(10)
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

            # while waiting for BOTH inference threads to complete, lets read gps data
            gps_data = gps.get_gps_data()
            
            # wait for inference completion
            inference_done.wait() # wait for inferences to complete
            
            # print raw results from lines inference (debugging)
            print("time: {:4f} | can overtake: {} | overtaking: {}".format(time.time()-start,global_vars.can_overtake_lanes.value, global_vars.overtaking.value))
        
            # aplicamos un "LPF", consideramos que estamos pasando solo si en los ultimos dos cuadros la red dijo que estabamos pasando
            #overtaking = prev_frame_overtaking and global_vars.overtaking.value
            overtaking.append(global_vars.overtaking.value)
            overtaking.pop(0) # remove oldest element
            overtaking_now = sum(overtaking) >= 2 # there are 2 or more True in the list

            # check if an infraction is taking place
            if overtaking_now and not was_overtaking and (not global_vars.can_overtake_lanes.value):# or not global_vars.can_overtake_signs.value):
                print("OVERTAKING, saving data")
                alert_event.set()
                #save_infraction(frame, time.strftime("%Y%m%d"),time.strftime("%H%M%S"), gps_data)
                inf = Infraction(cfg.plate, time.strftime("%Y%m%d"), time.strftime("%H%M%S"), gps_data, frame)
                save_infraction(inf)
            # update filter variables
            #prev_frame_overtaking = global_vars.overtaking.value  # retain previous value of global_vars.overtaking
            was_overtaking = overtaking                     # retain value of overtaking

main()

