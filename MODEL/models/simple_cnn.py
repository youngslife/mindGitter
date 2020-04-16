import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras.regularizers import l2

def SimpleCNN(num_features, num_labels, size):
  model = Sequential()
  model.add(Conv2D(num_features, kernel_size=(3, 3), 
  activation='relu', input_shape=(size[0], size[1], 1), 
  data_format='channels_last', kernel_regularizer=l2(0.01)))
  model.add(Conv2D(num_features, kernel_size=(3, 3), activation='relu'))
  model.add(Dropout(0.4))
  model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
  model.add(Conv2D(2*num_features, kernel_size=(3, 3), activation='relu'))
  model.add(Conv2D(2*num_features, kernel_size=(3, 3), activation='relu'))
  model.add(Dropout(0.4))
  model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
  model.add(Conv2D(2*2*num_features, kernel_size=(3, 3), activation='relu'))
  model.add(Conv2D(2*2*num_features, kernel_size=(3, 3), activation='relu'))
  model.add(Dropout(0.4))
  model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
  model.add(Flatten())

  model.add(Dense(2*2*num_features, activation='relu'))
  model.add(Dropout(0.5))
  model.add(Dense(2*num_features, activation='relu'))
  model.add(Dropout(0.4))
  model.add(Dense(num_labels, activation='softmax'))
  return model