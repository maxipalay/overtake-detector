import multiprocessing as mp
import time
from cv.lanes.lanes_detection import lines_detect
from cv.signs.signs_detection import signs_detect
import cv2
import numpy as np
import global_vars
global_vars.init()

# declare non global vars
current_time = None
gps_data = None

# sychronization mechanisms
image_ready = mp.Barrier(3)       # barrier that indicated data is ready
inference_done = mp.Barrier(3)   # barrier that indicated inference on both networks is done

process_lanes = mp.Process(name="lanes_detect", target=lines_detect, daemon=True, args=(image_ready, inference_done,))
process_signs = mp.Process(name="signs_detect", target=signs_detect, daemon=True, args=(image_ready, inference_done,))
process_lanes.start()
process_signs.start()

def main():
    counter = 0
    # load video
    cap=cv2.VideoCapture('/Users/maximilianopalay/Documents/UM/2020s2/TICV/street_images/ruta.mov')
    while(cap.isOpened()):
        for i in range(2050):
            ret, frame = cap.read()
        break
    
    while (cap.isOpened()):
        start=time.time()
        # first capture image and release inference threads
        ret, frame = cap.read()
        if ret == False:
            break
        frame = frame[60:660,500:1100,:]
        frame2 = cv2.resize(frame, (224,224), cv2.INTER_LINEAR)
        frame_input = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        #print(global_vars.image)
        global_vars.image[:]=frame_input.reshape(224*224*3)
        
        cv2.imshow('input',np.frombuffer(global_vars.image).reshape(224,224,3).astype(np.uint8)) #debug
        cv2.waitKey(1) & 0xFF      #debug
        #print ("image ready")      #debug

        image_ready.wait()   # release inference threads

        # while waiting for BOTH inference threads to complete, lets read gps data and current time
        
        #gps_data = ...
        current_time = time.time()

        
        # wait for inference completion
        
        #print("main waiting for results...")
        inference_done.wait() # wait for inferences to complete
        #print("main signaled inference done")
        print("time: {:4f} | can overtake: {} | overtaking: {}".format(time.time()-start,global_vars.can_overtake_lanes.value, global_vars.overtaking.value))
        
        # process everything
            # actions

        counter += time.time()-start
    print()
    print()
    print()
    print("average time "+str(counter/100))


main()
'''
IDEAS
programa principal -> leer camara, pasar a red neuronal lineas, pasar a red neuronal carteles,
comparar resultados y definir si se puede pasar o no
si esta sobrepasando y no se puede, tenemos que guardar foto y datos gps

poner un hilo que haga logging de los datos del gps cada cierto intervalo de tiempo
poner un hilo que haga un monitoreo de la velocidad, y se ocupe de ver los maximos y minimos

hilos
send_data_thread()  # checks for wifi connection, if it finds one it will try to send recorded data
camera_thread()     # starts camera object and reads frames continuously, putting them in a shared var
lines_detect_thread() # road lines detection
signs_detect_thread() # signs detection
alerts_thread()
gps_logger_thread()


'''
