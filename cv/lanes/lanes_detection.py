# quick workaround to import grandparent-directory
import sys
sys.path.append("...")
import global_vars
from time import sleep
import numpy as np
import tensorflow.lite as tflite
import tensorflow.keras.preprocessing as tfprep

def lines_detect_thread(image_ready, inference_done):
    # Load the TFLite model and allocate tensors.
    interpreter = tflite.Interpreter(model_path="cv/lanes/models/model.tflite", num_threads=4)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    while True:
        #print("lines_detect_thread waiting to execute...") #debug
        image_ready.wait() # wait for image to be ready
        #print("lines_detect_thread executing") #debug

        frame_input = tfprep.image.img_to_array(global_vars.image)
        frame_input = np.array([frame_input])  # Convert single image to a batch.
        
        interpreter.set_tensor(input_details[0]['index'], frame_input)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])[0,:,:,:]
        
        predictions[predictions<0.9] = 0
        predictions[predictions>=0.9] = 255
       
        #process predictions
        
        global_vars.overtaking = True
        global_vars.can_overtake_lanes = False

        #print("lines_detect_thread finished") #debug
        inference_done.wait()   # inference finished
