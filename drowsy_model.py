#code is from: https://www.kaggle.com/code/allelbhagya/cnn-99-5-accuracy/notebook


import pandas as pd #for data handling
import numpy as np #for number stuff
import tensorflow as tf #ML/AI
from tensorflow.keras.preprocessing.image import ImageDataGenerator #... edits image?
import matplotlib.pyplot as plt #plotting data

target = (96,96) # size of image

data_generator = ImageDataGenerator(rescale=1/.255, #editting size
                                     shear_range = 0.2,  #tilting of image
                                      horizontal_flip = True) #why does it horzontally flip it?
#this whole thing ^ generates the data.
#sfar as I can tell it's supposed to edit the existing data according to 
#GB

test_generator = ImageDataGenerator(rescale=1/.255,
                                     shear_range = 0.2,
                                      horizontal_flip = True)
#^ same thing but for test generator GB

train_data = data_generator.flow_from_directory('./data/train/', #path
                                                target_size=target, #img size
                                                color_mode='grayscale', #removing color
                                                class_mode='categorical', #classes...? But there's only 2 classes so why not binary
                                                batch_size = 256) #number of pics i presume...
test_data = test_generator.flow_from_directory('./data/test/',
                                                target_size=target,
                                                color_mode='grayscale',
                                                batch_size = 256,
                                                class_mode='categorical')
validation_data = data_generator.flow_from_directory('./data/val/',
                                                target_size=target,
                                                color_mode='grayscale',
                                                class_mode='categorical',
                                                batch_size = 256)

import keras #for buliding cnn
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization

from keras.models import Sequential #that's the model chosen.

model = Sequential()
#adds a layer: this one 
model.add(Conv2D(32, (3,3), #? GB
                 activation = 'relu', #removes negative values.???? GB
                 input_shape = (96,96,1) #shape of imgs, I presume))
model.add(MaxPooling2D(2,2)) #reducing resolution?
model.add(Conv2D(64, (3,3), activation = 'relu'))
model.add(MaxPooling2D(2,2))
model.add(Conv2D(128, (3,3), activation = 'relu'))
model.add(MaxPooling2D(2,2))
model.summary()
                 # so as far as I can tell, all these are layers of the NN

model.add(Flatten()) #1D array
model.add(Dense(128, activation = 'relu')) #128 = features in the output of model...
model.add(Dropout(0.3)) #prevents overfitting.
#^ randomly sets input units to 0 at a rate of 0.3.
model.add(Dense(2, activation = 'softmax')) #normalizes inputs...
model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
#^ training your model? optimizes your weights...?
#adam -- optimizer method
#loss -- error bet. model's predicted output v/s target values. binary, bcuz this is a yes/no model.
#metric -- to judge performance of model. kinda like loss. this is for human-understandable...
model.summary() #summary about NN

model.fit(train_data, validation_data = validation_data, epochs=20)
#epoch -- number of times gone through dataset.

model.save('drowsiness.h5') #saving the model, I'm guessing.

from keras.models import load_model

model = load_model('./drowsiness.h5')

model.evaluate(test_data)  #returns loss and metrics to assess model performance