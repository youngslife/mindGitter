import os
import pandas as pd
import numpy as np
from config import args
from sklearn.model_selection import train_test_split

def load_data(argname):
  try:
    data = pd.read_csv(args.dataset_path)
    return data
  except:
    print('Dataset path is not valid. Check out your logs.')

def handle_image():
  base_dir = os.path.join(args.data_dir, args.name)
  xtrain_dir = os.path.join(base_dir, 'xtrain.npy')
  ytrain_dir = os.path.join(base_dir, 'ytrain.npy')
  
  xvalid_dir = os.path.join(base_dir, 'xvalid.npy')
  yvalid_dir = os.path.join(base_dir, 'yvalid.npy')

  xtest_dir = os.path.join(base_dir, 'xtest.npy')
  ytest_dir = os.path.join(base_dir, 'ytest.npy')


  if os.path.isfile(xtrain_dir):
    xtrain = np.load(xtrain_dir)
    ytrain = np.load(ytrain_dir)
    xvalid = np.load(xvalid_dir)
    yvalid = np.load(yvalid_dir)
    print(f"Dataset was already preprocessed. Load existing xtrain and ytrain from {base_dir}")
    return xtrain, xvalid, ytrain, yvalid
  
  else: 
    data = load_data(args.name)
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
    print(X_train.shape)
    #saving the data samples to be used later
    np.save(xtrain_dir, X_train)
    np.save(ytrain_dir, y_train)
    np.save(xvalid_dir, X_valid)
    np.save(yvalid_dir, y_valid)
    np.save(xtest_dir, X_test)
    np.save(ytest_dir, y_test)
    print(f'train, valid, test data stored in {args.data_dir}//{args.name} respectively')

    return X_train, X_valid, y_train, y_valid

def handle_video():
  pass