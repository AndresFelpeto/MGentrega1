# -*- coding: utf-8 -*-
"""MGtrabajo1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10WTGUGIRe2exNh0bQGFtIZldi39mQb32
"""

from google.colab import files
files.upload()

!mkdir -p ~/.kaggle
!mv kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle competitions download -c mg-animal-prediction-24-25

!unzip mg-animal-prediction-24-25.zip

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from PIL import Image

train_images= 'train_images/train_images/train_images'
test_images= 'test_images/test_images/test_images'
img_size = (100, 100)
batch_size = 50

datagen = ImageDataGenerator(rescale=1.0/255.0,validation_split=0.2)
train_generator = datagen.flow_from_directory(
    train_images,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='sparse',
    color_mode='grayscale',
    subset='training'
)
print(len(train_generator))

plt.imshow(train_generator[0][0][0])

plt.show()

input_layer = tf.keras.Input(shape=(100, 100, 1))
x = tf.keras.layers.Conv2D(8, (3, 3), activation='relu')(input_layer)
x = tf.keras.layers.Conv2D(16, (3, 3), activation='relu')(x)
x = tf.keras.layers.Conv2D(32, (3, 3), activation='relu')(x)
x = tf.keras.layers.Flatten()(x)
x = tf.keras.layers.Dense(8, activation='relu')(x)
output_layer = tf.keras.layers.Dense(10, activation='softmax')(x)
model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
model.summary()

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy', # etiquetas como números, no onehot
              metrics=['accuracy']
            )

history = model.fit(train_generator, epochs=10)

def plot_metric(data, what):
  plt.figure(figsize=(10, 5))
  plt.plot(data[what])
  plt.plot(data['val_' + what])
  plt.title('model ' + what)
  plt.ylabel(what)
  plt.xlabel('epoch')
  plt.legend(['train', 'validation'], loc='upper left')

plot_metric(history.history, 'accuracy')
plot_metric(history.history, 'loss')