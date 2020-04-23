import os, subprocess, cv2, glob, pickle
import pandas as pd
import numpy as np
from shutil import rmtree
from config import args
from sklearn.model_selection import train_test_split

def load_original_data():
  try:
    data = pd.read_csv(args.dataset_path)
    return data
  except:
    print('Dataset path is not valid. Check out your logs.')

def csv_to_npy(s):
  data = pd.read_csv(s, header=None)
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
  return X

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
  

def handle_dir():
  if os.path.exists(os.path.join(args.v_work)):
    rmtree(args.v_work)
  if os.path.exists(args.frames_dir):
    rmtree(os.path.join(args.frames_dir))
  if os.path.exists(args.crop_dir):
    rmtree(args.crop_dir)
  
  os.makedirs(args.v_work)
  os.makedirs(args.frames_dir)
  os.makedirs(args.crop_dir)


def extract_frames():
  try:
    command = ("ffmpeg -y -i %s -qscale:v 2 -async 1 -r 10 %s" % (args.dataset_path, os.path.join(args.v_work, 'video.avi')))
    output = subprocess.call(command, stdout=None)
    command = ("ffmpeg -y -i %s -qscale:v 2 -threads 1 -f image2 %s" % (os.path.join(args.v_work, 'video.avi'), os.path.join(args.frames_dir,'%06d.jpg'))) 
    output = subprocess.call(command, stdout=None)
    command = ("ffmpeg -y -i %s -ac 1 -vn -acodec pcm_s16le -ar 16000 %s" % (os.path.join(args.v_work,'video.avi'), os.path.join(args.v_work,'audio.wav'))) 
    output = subprocess.call(command, stdout=None) # ar 은 frame과 상관이있나?
  except:
    raise ValueError('Fail to convert the video and extract frames. Check the video and options.')


def face_detection():
  print("Loading face detection model")
  net = cv2.dnn.readNetFromCaffe(os.path.join(args.model_dir, 'deploy.prototxt.txt'), os.path.join(args.model_dir, 'res10_300x300_ssd_iter_140000_fp16.caffemodel'))
  flist = glob.glob(os.path.join(args.frames_dir,'*.jpg'))
  flist.sort()
  
  dets = []
  for fidx, fname in enumerate(flist):
    image = cv2.imread(fname)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (103.93, 116.77, 123.68))
    net.setInput(blob)
    detections = net.forward()

    # dets.append([])
    for i in range(0, detections.shape[2]):
      confidence = detections[0, 0, i, 2]
      if confidence > 0.5:
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        startX, startY, endX, endY = box.astype("int")
        dets.append({'frame':fidx, 'box':(startX, startY, endX, endY), 'conf':confidence})
  
  savepath = os.path.join(args.v_work, 'dets.pckl')
  with open(savepath, 'wb') as fil:
    pickle.dump(dets, fil)
  return dets

# crop 부분에 대한 음성을 추출하고 다시 crop부분과 합치는 파트 추가 필요 
def crop_video(track):
  flist = glob.glob(os.path.join(args.frames_dir, '*.jpg'))
  flist.sort()
  fourcc = cv2.VideoWriter_fourcc(*'XVID')
  v_out = cv2.VideoWriter(os.path.join(args.v_work, 'cropped.avi'), fourcc, 10, (300, 300))

  dets = {'x':[], 'y':[], 's':[]}
  for tdet in track:
    det = tdet['box']
    dets['s'].append(max((det[3]-det[1]),(det[2]-det[0]))/2)
    dets['y'].append((det[1]+det[3])/2)
    dets['x'].append((det[0]+det[2])/2)
  faces = []
  for fidx, tdet in enumerate(track):
    frame = tdet['frame']
    bs = dets['s'][fidx]
    image = cv2.imread(flist[frame])
    face = image[int(dets['y'][fidx]-bs):int(dets['y'][fidx]+bs), int(dets['x'][fidx]-bs):int(dets['x'][fidx]+bs)]
    cv2.imwrite(os.path.join(args.crop_dir, flist[frame][-10:]), face)
    v_out.write(cv2.resize(face, (300, 300)))
    faces.append(face)
  v_out.release()
  savepath = os.path.join(args.v_work, 'faces.pckl')
  # with open(savepath, 'wb') as fil:
  #   pickle.dump(dets, fil)
  # 음성 여기에 이어서
  return faces

def face_to_testdata(faces):
  face_npy = []
  for face in faces:
    f = cv2.resize(src=face, dsize=(48, 48), interpolation=cv2.INTER_AREA)
    f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    face_npy.append(f.astype('float32'))
  # ytest부분은 데이터셋이 오면 바뀔 예정
  face_npy = np.asarray(face_npy)
  
  face_npy = np.expand_dims(face_npy, -1)
  face_npy -= np.mean(face_npy, axis=0)
  face_npy /= np.std(face_npy, axis=0)

  ytest = [3] * len(faces)
  y = np.asarray(ytest).reshape(-1)
  ytest = np.eye(7)[y]

  np.save(args.xtest_dir, face_npy)
  np.save(args.ytest_dir, ytest)
  return face_npy, ytest

# 한사람이 한 화면에 정면을 바라보고 있는 것을 가정
# 여러 명의 얼굴을 분석하려면 face_tracking 파트가 필요
# 얼굴이 없는 프레임도 포함하려면 scenedetect 파트가 필요
def load_video():
  if args.is_data_video == 'False':
    raise ValueError('is_data_video options should be True. Check options again.')
  
  handle_dir()
  extract_frames()
  dets = face_detection()
  faces = crop_video(dets)
  xtest, ytest = face_to_testdata(faces)
  return xtest, ytest
  