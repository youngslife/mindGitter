import utils, os
import numpy as np
from data import preprocess, visualization
from config import args

from keras.optimizers import Adam
from models.simple_cnn import SimpleCNN
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.losses import categorical_crossentropy

# save configs
utils.save_logs()

# data preprocessing
if args.is_data_video == 'True':
  preprocess.load_video()
elif args.is_data_video == 'False':
  xtrain, xvalid, ytrain, yvalid = preprocess.load_image()
else:
  print('Check argument is data video. It must be True or False')


#hyper parameters
num_features = 64
num_labels = 7
size = (48, 48)
batch_size = 64
epochs = 35

# Select Model 
if args.model == 'sCNN':
  model = SimpleCNN(num_features, num_labels, size)
  model.summary()
else:
  raise ValueError(f'There is no valid model named {args.model}. Check again models.')

checkpoint = ModelCheckpoint(args.checkpoint_path, monitor='val_accuracy', save_best_only=True, save_weights_only=True, period=1)

if args.from_checkpoint == 'True':
  model.load_weights(checkpoint_path.format(epoch=0))

# 모델이 많아진다면 loss, optimizer 등의 하이퍼파라미터등도 인자화하거나 모델자체를 저장해야한다.
#Compliling the model with adam optimixer and categorical crossentropy loss
model.compile(loss=categorical_crossentropy,
              optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7),
              metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_accuracy', patience=3)
callback_list = [checkpoint, early_stopping]

# training the model
history = model.fit(np.array(xtrain), np.array(ytrain),
          batch_size=batch_size,
          epochs=epochs,
          callbacks=callback_list,
          verbose=1,
          validation_data=(np.array(xvalid), np.array(yvalid)),
          shuffle=True)

# visaulization of acc & loss on train data & validation data
if args.show_graphs == 'True':
  visualization.draw_accloss(history)
  