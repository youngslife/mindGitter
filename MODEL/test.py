import utils, os
import numpy as np
from config import args
from data import preprocess
from models.simple_cnn import SimpleCNN
from keras.optimizers import Adam
from keras.losses import categorical_crossentropy


if args.is_train == 'True':
  raise ValueError('You are trying to run test with train option. Check options again.')

# save configs
utils.save_logs()

# load dataset
if args.is_data_video == 'True':
  preprocess.load_video()
elif args.is_data_video == 'False':
  xtest, ytest = preprocess.load_image()

#hyper parameters
num_features = 64
num_labels = 7
size = (48, 48)
batch_size = 64
epochs = 15

# Select Model 
if args.model == 'sCNN':
  model = SimpleCNN(num_features, num_labels, size)
  model.load_weights(args.checkpoint_path)
  model.summary()
else:
  raise ValueError(f'There is no valid model named {args.model}. Check again models.')

model.compile(loss=categorical_crossentropy,
            optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7),
            metrics=['accuracy'])

# Evaluate the model on the test data using `evaluate`
print('\n# Evaluate on test data')
results = model.evaluate(xtest, ytest, batch_size=batch_size)
print('test loss, test acc:', results)

# Generate predictions (probabilities -- the output of the last layer)
# on new data using `predict`
print('\n# Generate predictions for 3 samples')
predictions = model.predict(xtest[:3])
print('predictions shape:', predictions.shape)