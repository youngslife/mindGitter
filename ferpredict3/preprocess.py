import pandas as pd
import numpy as np
import glob, cv2, subprocess

# def csv_to_npy(s):
#   data = pd.read_csv(s)
#   width, height = 48, 48
#   datapoints = data.values.tolist()

#   #getting features for training
#   X = []
#   for xseq in datapoints:
#     xx = [int(xp) for xp in xseq[0].split(' ')]
#     xx = np.asarray(xx).reshape(width, height)
#     X.append(xx.astype('float32'))
  
#   X = np.asarray(X)
#   X = np.expand_dims(X, -1)

#   #input regularization
#   X -= np.mean(X, axis=0)
#   X /= np.std(X, axis=0)
#   return X


def extract_frames(videoUrl):
  try:
    command = ("ffmpeg -y -i %s -qscale:v 2 -async 1 -r 1 %s" % (videoUrl, 'data/video.avi'))
    output = subprocess.call(command, shell=True, stdout=None)
    command = ("ffmpeg -y -i %s -qscale:v 2 -threads 1 -f image2 %s" % ('data/video.avi', 'data/frames/%06d.jpg'))
    output = subprocess.call(command, shell=True, stdout=None)
    command = ("ffmpeg -y -i %s -ac 1 -vn -acodec pcm_s16le -ar 16000 %s" % ('data/video.avi', 'data/audio.wav')) 
    output = subprocess.call(command, shell=True, stdout=None) # ar 은 frame과 상관이있나?
  except:
    raise ValueError('Fail to convert the video and extract frames. Check the video and options.')


def face_detection():
  print("Loading face detection model")
  net = cv2.dnn.readNetFromCaffe('models/deploy.prototxt.txt', 'models/res10_300x300_ssd_iter_140000_fp16.caffemodel')
  flist = glob.glob('data/frames/*.jpg')
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
  
  return dets

# crop 부분에 대한 음성을 추출하고 다시 crop부분과 합치는 파트 추가 필요 
def crop_video(track):
  flist = glob.glob('data/frames/*.jpg')
  flist.sort()
  fourcc = cv2.VideoWriter_fourcc(*'XVID')
  v_out = cv2.VideoWriter('data/cropped.avi', fourcc, 1, (300, 300))

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
    # cv2.imwrite(os.path.join(args.crop_dir, flist[frame][-10:]), face)
    v_out.write(cv2.resize(face, (300, 300)))
    faces.append(face)
  v_out.release()
  # savepath = os.path.join(args.v_work, 'faces.pckl')
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
  face_npy = np.asarray(face_npy)
  
  face_npy = np.expand_dims(face_npy, -1)
  face_npy -= np.mean(face_npy, axis=0)
  face_npy /= np.std(face_npy, axis=0)

  return face_npy

# 한사람이 한 화면에 정면을 바라보고 있는 것을 가정
# 여러 명의 얼굴을 분석하려면 face_tracking 파트가 필요
# 얼굴이 없는 프레임도 포함하려면 scenedetect 파트가 필요
def video_to_npy(url):
  print(url)
  extract_frames(url)
  dets = face_detection()
  faces = crop_video(dets)
  xtest = face_to_testdata(faces)
  return xtest
  