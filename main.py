import threading
import time
from cv.lanes.lanes_detection import lines_detect_thread
from cv.signs.signs_detection import signs_detect_thread
import cv2

import global_vars
global_vars.init()

# declare non global vars
current_time = None
gps_data = None

# sychronization mechanisms
image_ready = threading.Barrier(3)       # barrier that indicated data is ready
inference_done = threading.Barrier(3)   # barrier that indicated inference on both networks is done

# declare & fire inference threads
thread2 = threading.Thread(name="lanes_detect", target=lines_detect_thread, daemon=True, args=(image_ready, inference_done,))
thread3 = threading.Thread(name="signs_detect", target=signs_detect_thread, daemon=True, args=(image_ready, inference_done,))
thread2.start()
thread3.start()

def main():
    global_vars.image = 0
    counter = 0
    
    # load video
    cap=cv2.VideoCapture('/Users/maximilianopalay/Documents/UM/2020s2/TICV/street_images/ruta.mov')
    while(cap.isOpened()):
        for i in range(240):
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
        global_vars.image=frame_input
        print ("image ready")

        image_ready.wait()   # release inference threads

        # while waiting for BOTH inference threads to complete, lets read gps data and current time
        
        #gps_data = ...
        current_time = time.time()

        
        # wait for inference completion
        
        print("main waiting for results...")
        inference_done.wait() # wait for inferences to complete
        print("main signaled inference done")
        
        # process everything
            # actions

        print(str(time.time()-start))
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
