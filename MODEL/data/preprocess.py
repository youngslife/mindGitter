import os
import pandas as pd
import numpy as np
from config import args
from sklearn.model_selection import train_test_split

def load_original_data():
  try:
    data = pd.read_csv(args.dataset_path)
    return data
  except:
    print('Dataset path is not valid. Check out your logs.')


def split_original_data(data):
  try:
    width, height = 48, 48
    datapoints = data['pixels'].tolist()

    #getting features for training
    X = []
    for xseq in datapoints:
      xx = [int(xp) for xp in xseq.split(' ')]
      xx = np.asarray(xx).reshape(width, height)
      X.append(xx.astype('float32'))
    
    X = np.asarray(X)
    X = np.expand_dims(X, -1)

    #input regularization
    X -= np.mean(X, axis=0)
    X /= np.std(X, axis=0)
    #getting labels for training
    y = pd.get_dummies(data['emotion'])
    y = y.to_numpy()

    #storing them using numpy
    print("Preprocessing Done")
    print("Number of Features: "+str(len(X[0])))
    print("Number of Labels: "+ str(len(y[0])))
    print("Number of examples in dataset: "+str(len(X)))
    print(f"X,y stored in fdataX.npy and flabels.npy in {args.data_dir}//{args.name} respectively")
    
    print("Splitting into training, validation and testing data. The ratio is train : valid : test = 8 : 1 : 1")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.1, random_state=41)

    #saving the data samples to be used later
    np.save(args.xtrain_dir, X_train)
    np.save(args.ytrain_dir, y_train)
    np.save(args.xvalid_dir, X_valid)
    np.save(args.yvalid_dir, y_valid)
    np.save(args.xtest_dir, X_test)
    np.save(args.ytest_dir, y_test)
    print(f'train, valid, test data stored in {args.data_dir}//{args.name} respectively')
  except:
    raise ValueError('Error duringsplit_original_data')


def load_image():
  if not os.path.isfile(args.xtrain_dir):
    data = load_original_data()
    split_original_data(data)
  else:
    print(f"Dataset was already preprocessed. Load existing xtrain and ytrain from {args.data_dir}//{args.name}")
  
  X_train = np.load(args.xtrain_dir)
  y_train = np.load(args.ytrain_dir)
  X_valid = np.load(args.xvalid_dir)
  y_valid = np.load(args.yvalid_dir)
  X_test = np.load(args.xtest_dir)
  y_test = np.load(args.ytest_dir)

  if args.is_train == 'True':
    return X_train, X_valid, y_train, y_valid
  elif args.is_train == 'False':
    return X_test, y_test
  else:
    raise ValueError('Is_train should True or False. Check options again.')
  

def load_video():
  pass