# run inference on one picture example

import tensorflow as tf
import numpy as np
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import itertools
from tensorflow.keras.preprocessing.image import img_to_array, load_img

model_path = "" # path to model e.g. "./folder/model.h5"
img_path = "" 	# path to image to run inference on e.g. "./folder/picture.png"
mask_path = "" 	# path to mask corresponding to image e.g. "./folder/mask.png"

model = tf.keras.models.load_model(model_path)

input_height=224
input_width=224
# make predictions on the testing images, finding the index of the
# label with the corresponding largest predicted probability
image = tf.keras.preprocessing.image.load_img(img_path, target_size=(input_height,input_width), interpolation="nearest", color_mode='rgb')
input_arr = tf.keras.preprocessing.image.img_to_array(image)
input_arr = np.array([input_arr])  # Convert single image to a batch.
image_truth = tf.keras.preprocessing.image.load_img(mask_path, target_size=(input_height,input_width), interpolation="nearest", color_mode='grayscale')
image_truth = tf.keras.preprocessing.image.img_to_array(image_truth)
image_truth = np.array([image_truth])
predictions = model.predict(input_arr)

# prediction 8
plt.subplot(121)
plt.imshow(predictions[0,:,:,0], cmap='gray', vmin=0, vmax=1)
plt.subplot(122)
plt.imshow(input_arr[0,:,:,:]/255)
