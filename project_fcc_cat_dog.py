# -*- coding: utf-8 -*-
"""project_fcc_cat_dog.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xq7W7Q7kozBsSxGLJ1NtpmTu1dtd9ve_
"""

# Commented out IPython magic to ensure Python compatibility.
try:
  # This command only in Colab.
#   %tensorflow_version 2.x
except Exception:
  pass
import tensorflow as tf
import pandas as pd

from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
import numpy as np
import matplotlib.pyplot as plt

# Get project files
!wget https://cdn.freecodecamp.org/project-data/cats-and-dogs/cats_and_dogs.zip

!unzip cats_and_dogs.zip

PATH = 'cats_and_dogs'

train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')
test_dir = os.path.join(PATH, 'test')

# Get number of files in each directory. The train and validation directories
# each have the subdirecories "dogs" and "cats".
total_train = sum([len(files) for r, d, files in os.walk(train_dir)])
total_val = sum([len(files) for r, d, files in os.walk(validation_dir)])
total_test = len(os.listdir(test_dir))

# Variables for pre-processing and training.
batch_size = 128
epochs = 15
IMG_HEIGHT = 150
IMG_WIDTH = 150

print(test_dir)

# 3
train_image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale = 1./255)
validation_image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale = 1./255)
test_image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale = 1./255)

train_data_gen = train_image_generator.flow_from_directory(train_dir,
                                                           target_size=(150, 150),
                                                           batch_size=batch_size,
                                                           class_mode='binary')

val_data_gen = validation_image_generator.flow_from_directory(validation_dir,
                                                           target_size=(150, 150),
                                                           batch_size=batch_size,
                                                           class_mode='binary')

test_data_gen = test_image_generator.flow_from_directory('cats_and_dogs/test',
                                                         target_size = (150, 150),
                                                         shuffle = False,
                                                         class_mode = None)

# 4
def plotImages(images_arr, probabilities = False):
    fig, axes = plt.subplots(len(images_arr), 1, figsize=(5,len(images_arr) * 3))
    if probabilities is False:
      for img, ax in zip( images_arr, axes):
          ax.imshow(img)
          ax.axis('off')
    else:
      for img, probability, ax in zip( images_arr, probabilities, axes):
          ax.imshow(img)
          ax.axis('off')
          if probability > 0.5:
              ax.set_title("%.2f" % (probability*100) + "% dog")
          else:
              ax.set_title("%.2f" % ((1-probability)*100) + "% cat")
    plt.show()

sample_training_images, _ = next(train_data_gen)
plotImages(sample_training_images[:5])

# 5
train_image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rotation_range = 40,
                                                                        width_shift_range = 0.2,
                                                                        height_shift_range = 0.2,
                                                                        zoom_range = 0.2,
                                                                        fill_mode = 'nearest',
                                                                        rescale = 1./255)

# 6
train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                     directory=train_dir,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                     class_mode='binary')

augmented_images = [train_data_gen[0][0][0] for i in range(5)]

plotImages(augmented_images)

# 7
model = Sequential()

model.add(Conv2D(32,(3,3), input_shape = (150,150,3), activation = 'relu'))
model.add(MaxPooling2D())

model.add(Conv2D(32,(3,3), activation = 'relu'))
model.add(MaxPooling2D())

model.add(Conv2D(64,(3,3), strides = (1,1), activation = 'relu'))
model.add(MaxPooling2D())

model.add(Flatten())
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.3))
model.add(Dense(1, activation = 'sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='Adam',
              metrics=['accuracy'])


model.summary()

# 8
history = model.fit(
    train_data_gen,
    epochs = epochs,
    batch_size = batch_size,
    validation_data = val_data_gen
)

# 9
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

probabilities = model.predict(test_data_gen)

# 11
answers =  [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0,
            1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0,
            1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1,
            0, 0, 0, 0, 0, 0]

correct = 0

for probability, answer in zip(probabilities, answers):
  if round(probability[0]) == answer:
    correct +=1

percentage_identified = (correct / len(answers)) * 100

passed_challenge = percentage_identified >= 63

print(f"Your model correctly identified {round(percentage_identified, 2)}% of the images of cats and dogs.")

if passed_challenge:
  print("You passed the challenge!")
else:
  print("You haven't passed yet. Your model should identify at least 63% of the images. Keep trying. You will get it!")