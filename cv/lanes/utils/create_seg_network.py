# Create Segmentation Network for lane detection
# Some useful links that were useful to understand and implement an Encoder-Decoder architecture:
#   https://keras.io/examples/vision/oxford_pets_image_segmentation/
#   https://medium.com/@prince.canuma/how-to-do-image-segmentation-in-minutes-b49e15fa19f0
#   https://github.com/divamgupta/image-segmentation-keras
#   https://medium.com/@pallawi.ds/understand-semantic-segmentation-with-the-fully-convolutional-network-u-net-step-by-step-9d287b12c852
#   https://divamgupta.com/image-segmentation/2019/06/06/deep-learning-semantic-segmentation-keras.html
#   https://medium.com/@qucit/a-keras-segnet-implementation-for-building-detection-in-the-spacenet-dataset-edd23933f1f4
#   https://towardsdatascience.com/understanding-semantic-segmentation-with-unet-6be4f42d4b47
#   https://www.tensorflow.org/tutorials/images/segmentation



import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import *

# network input size (224, 224, 3) images
input_height = 224
input_width = 224

# number of classes
n_classes = 7

# build network

# first layer
img_input = Input(shape=(input_height, input_width, 3))

# Encoder layers

x = Convolution2D(64, (3, 3), activation='relu', padding='same',
               name='block1_conv1')(img_input)
x = Convolution2D(64, (3, 3), activation='relu', padding='same',
               name='block1_conv2')(x)
x = (BatchNormalization())(x)
x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

f1 = x

x = Convolution2D(128, (3, 3), activation='relu', padding='same',
               name='block2_conv1')(x)
x = Convolution2D(128, (3, 3), activation='relu', padding='same',
               name='block2_conv2')(x)
x = (BatchNormalization())(x)
x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

f2 = x

x = Convolution2D(256, (3, 3), activation='relu', padding='same',
               name='block3_conv1')(x)
x = Convolution2D(256, (3, 3), activation='relu', padding='same',
               name='block3_conv2')(x)
#x = Convolution2D(256, (3, 3), activation='relu', padding='same',
#               name='block3_conv3')(x)
x = (BatchNormalization())(x)
x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

f3 = x

x = Convolution2D(512, (3, 3), activation='relu', padding='same',
               name='block4_conv1')(x)
x = Convolution2D(512, (3, 3), activation='relu', padding='same',
               name='block4_conv2')(x)
#x = Convolution2D(512, (3, 3), activation='relu', padding='same',
#               name='block4_conv3')(x)
x = (BatchNormalization())(x)
x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

# Decoder layers

o = (UpSampling2D((2, 2)))(x)

o = Convolution2D(512, (3, 3), activation='relu', padding='same',
               name='block5_conv1')(o)
o = Convolution2D(512, (3, 3), activation='relu', padding='same',
               name='block5_conv2')(o)
#o = Convolution2D(512, (3, 3), activation='relu', padding='same',
#               name='block5_conv3')(o)
o = (BatchNormalization())(o)


o = (concatenate([o, f3], axis=-1))


o = (UpSampling2D((2, 2)))(o)

o = Convolution2D(256, (3, 3), activation='relu', padding='same',
               name='block6_conv1')(o)
o = Convolution2D(256, (3, 3), activation='relu', padding='same',
               name='block6_conv2')(o)
#o = Convolution2D(256, (3, 3), activation='relu', padding='same',
#               name='block6_conv3')(o)

o = (BatchNormalization())(o)

o = (concatenate([o, f2], axis=-1))


o = (UpSampling2D((2, 2)))(o)

o = Convolution2D(128, (3, 3), activation='relu', padding='same',
               name='block7_conv1')(o)
o = Convolution2D(128, (3, 3), activation='relu', padding='same',
               name='block7_conv2')(o)

o = (BatchNormalization())(o)

o = (concatenate([o, f1], axis=-1))

o = (UpSampling2D((2, 2)))(o)

o = Convolution2D(64, (3, 3), activation='relu', padding='same',
               name='block8_conv1')(o)
o = Convolution2D(n_classes, (3, 3), activation='relu', padding='same',
               name='block8_conv2')(o)

o = (BatchNormalization())(o)

# activation layer

o = (Activation('softmax'))(o)

# model compilation and saving

model = Model(img_input, o)

model.compile(
  optimizer="rmsprop", loss="sparse_categorical_crossentropy", metrics=[tf.metrics.SparseCategoricalCrossentropy(), tf.metrics.SparseCategoricalAccuracy()])
model.save('lines_detector.h5')
model.summary()


