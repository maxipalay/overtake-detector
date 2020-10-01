import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from tensorflow.keras.callbacks import ModelCheckpoint

# open network file
model = tf.keras.models.load_model("lines_detector.h5", custom_objects=None)

# network input width & height
input_height = 224
input_width = 224

# paths for training data
training_images_path = '../../../../test_dataset/training/images'
training_gtruth_path = '../../../../test_dataset/training/gtruth'

# paths for validation data
validation_images_path = '../../../../test_dataset/validation/images'
validation_gtruth_path = '../../../../test_dataset/validation/gtruth'

# training data generator
train_image_datagen = ImageDataGenerator(brightness_range = (0.9,1.1))
train_mask_datagen = ImageDataGenerator()
seed=1
train_image_generator = train_image_datagen.flow_from_directory(
    training_images_path,
    target_size=(input_height, input_width),
    interpolation="nearest",
    class_mode=None,
    batch_size=16,
    shuffle=False, seed=seed)
train_mask_generator = train_mask_datagen.flow_from_directory(
    training_gtruth_path,
    target_size=(input_height, input_width),
    interpolation="nearest",
    class_mode=None,
    batch_size=16,
    shuffle=False,
    color_mode='grayscale', seed=seed)

# validation data generator
val_image_datagen = ImageDataGenerator()
val_mask_datagen = ImageDataGenerator()
seed=1
val_image_generator = val_image_datagen.flow_from_directory(
    validation_images_path,
    target_size=(input_height, input_width),
    interpolation="nearest",
    class_mode=None,
    batch_size=2,
    shuffle=False, seed=seed)
val_mask_generator = val_mask_datagen.flow_from_directory(
    validation_gtruth_path,
    target_size=(input_height, input_width),
    interpolation="nearest",
    class_mode=None,
    batch_size=2,
    shuffle=False,
    color_mode='grayscale', seed=seed)

# combine generators into one which yields image and masks
train_generator = zip(train_image_generator, train_mask_generator)
val_generator = zip(val_image_generator, val_mask_generator)

# train

checkpoint = ModelCheckpoint(filepath='model.{epoch:02d}-{val_loss:.2f}.h5', save_freq="epoch", verbose=1)

model.fit(train_generator, epochs=10, steps_per_epoch=92, validation_data=val_generator, validation_steps=31, callbacks=[checkpoint])
