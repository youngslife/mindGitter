import utils, os
import numpy as np
from config import args
from data import preprocess, visualization

from keras.optimizers import Adam
from models.simple_cnn import SimpleCNN
from keras.losses import categorical_crossentropy
from sklearn.metrics import confusion_matrix, classification_report


if args.is_train == 'True':
  raise ValueError('You are trying to run test with train option. Check options again.')

# save configs
utils.save_logs()

# load dataset
if args.is_data_video == 'True':
  preprocess.load_video()
elif args.is_data_video == 'False':
  xtest, ytest = preprocess.load_image()
else:
  print('Check argument is data video. It must be True or False')

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

# predict the model on the test data using predict
yh = model.predict(xtest)

yh = yh.tolist()
yt = ytest.tolist()

truey = [yt[i].index(max(yt[i])) for i in range(len(ytest))]
predy = [yh[i].index(max(yh[i])) for i in range(len(ytest))]

np.save(args.truey_dir, truey)
np.save(args.predy_dir, predy)
print("Predicted and true label values saved")

# confusion matrix & report
cm = confusion_matrix(truey, predy)
cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
cr = classification_report(truey, predy)
print(cm)
print(cr)

# visualization
if args.show_graphs == 'True':
  visualization.draw_confusion_matrix(cm)
  visualization.draw_pred_sample(xtest, ytest, truey, predy, yh)

