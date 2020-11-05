# quick workaround to import grandparent-directory
import sys
sys.path.append("...")
import global_vars
import numpy as np
import tensorflow.lite as tflite
import tensorflow.keras.preprocessing as tfprep
from cv2 import GaussianBlur

def lines_detect(image_ready, inference_done):
    # Load the TFLite model and allocate tensors.
    interpreter = tflite.Interpreter(model_path="cv/lanes/models/model.tflite", num_threads=4)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    while True:
        #print("lines_detect waiting to execute...") #debug
        image_ready.wait() # wait for image to be ready
        #print("lines_detect executing") #debug
        frame_input = np.frombuffer(global_vars.image).reshape(224,224,3)

        frame_input = tfprep.image.img_to_array(frame_input)
        frame_input = np.array([frame_input])  # Convert single image to a batch.
        
        interpreter.set_tensor(input_details[0]['index'], frame_input)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])[0,:,:,:]
        

        #predictions[predictions<0.9] = 0
        #predictions[predictions>=0.9] = 255
      
        # red mask
        red_mask = predictions[:,:,4]+predictions[:,:,6]
        # green mask
        green_mask = predictions[:,:,3]+predictions[:,:,5]
        
        red_mask = GaussianBlur(red_mask, (3,3), 0)
        red_mask[red_mask<0.8] = 0
        red_mask[red_mask>=0.8] = 255
        green_mask = GaussianBlur(green_mask, (3,3), 0)
        green_mask[green_mask<0.8] = 0
        green_mask[green_mask>=0.8] = 255
        
        red_norm = np.linalg.norm(red_mask)
        green_norm = np.linalg.norm(green_mask)
        can_overtake = green_norm>=red_norm
        overtaking=False
        if can_overtake:
            # trabajo con green_mask
            (rows,cols)=np.where(green_mask==255) # busco los indices de las posiciones donde esta presente el color verde
            rows_indices = [index for index,elem in enumerate(rows) if elem==rows[-1]]
            cols_indices = cols[rows_indices] # agarro los indices de las columnas donde hay mascara verde (pero solo los de la fila de mas abajo)
            if rows_indices:
                colsmin = min(cols_indices)
                colsmax = max(cols_indices)
                midpoint = (colsmax-colsmin)/2+colsmin
                if midpoint>112:
                    overtaking=True
                else:
                    overtaking=False
        else:
            # trabajo con red_mask
            (rows,cols)=np.where(red_mask==255)
            rows_indices = [index for index,elem in enumerate(rows) if elem==rows[-1]]
            cols_indices = cols[rows_indices]
            if rows_indices:
                colsmin = min(cols_indices)
                colsmax = max(cols_indices)
                midpoint = (colsmax-colsmin)/2+colsmin
                if midpoint>112:
                    overtaking=True
                else:
                    overtaking=False
        
        #print("can overtake: "+str(can_overtake))
        #print("overtaking: "+str(overtaking))

        global_vars.can_overtake_lanes.value = can_overtake
        global_vars.overtaking.value = overtaking

        #print("lines_detect finished") #debug
        inference_done.wait()   # inference finished
