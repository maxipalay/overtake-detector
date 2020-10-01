# convert frozen model to tensorflow lite
import numpy as np
import os
import tensorflow as tf

validation_images_path = "../../../../test_dataset/validation/images/images"

model = tf.keras.models.load_model("../../../../lines_detector.h5")
(input_height,input_width)=(224,224)
files = os.listdir(validation_images_path)
files = [validation_images_path+'/'+x for x in files if x.split(".")[-1]=="png" ]
files.sort()
def representative_dataset_gen():
    for i in range(10):
        test_image = tf.keras.preprocessing.image.load_img(files[i], target_size=(input_height,input_width), interpolation="nearest", color_mode='rgb')
        test_image = tf.keras.preprocessing.image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        yield [test_image]


# convert to tflite with optimization considering sample dataset
converter3 = tf.lite.TFLiteConverter.from_keras_model(model)# convert to tflite with optimizations
converter3.optimizations = [tf.lite.Optimize.DEFAULT]

converter3.representative_dataset = representative_dataset_gen

converted_tflite_model_opt_with_dataset = converter3.convert()

with tf.io.gfile.GFile('model.tflite', 'wb') as f:
  f.write(converted_tflite_model_opt_with_dataset)

