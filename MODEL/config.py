import argparse, os
from datetime import datetime

parser = argparse.ArgumentParser(description="Set configuration for FER model")
parser.add_argument('--timestamp', type=str, default=str(datetime.now().strftime("%Y%m%d%H%M%S")))
parser.add_argument('--name', required=True, type=str, help='The unit of project. Name folder under data will be created to store outcomes when you run models.')
parser.add_argument('--model', type=str, help='The model you want to use to face emotion recognition. There is only sCNN now.')
parser.add_argument('--model_dir', type=str, default='.\\models')
parser.add_argument('--is_train', type=str, default='True', help='If want to run test, it should be False')
parser.add_argument('--is_data_video', type=str, default='True', help='If data type is video, input True. Model will extract frames and audio')
parser.add_argument('--dataset_path', type=str, default='.\\datasets\\monoact.mp4', help='Path of dataset')
parser.add_argument('--data_dir', type=str, default='.\\data', help='dir path for output of the model')
parser.add_argument('--checkpoint_dir', type=str, default='.\\checkpoints', help='Base dir of Checkpoints. According to Options checkpoints_path will be created. e.g.checkpoints/name/train')
parser.add_argument('--from_checkpoint', type=str, default='False', help='Input True if want to train from the checkpoints')
parser.add_argument('--show_graphs', type=str, default='False', help='Input True if want to see graphs')
args = parser.parse_args()

base_dir = os.path.join(args.data_dir, args.name)
if args.is_data_video == 'True':
  setattr(args, 'v_work', os.path.join(base_dir, 'v_work'))
  setattr(args, 'frames_dir', os.path.join(base_dir, 'frames_dir'))
  setattr(args, 'crop_dir', os.path.join(base_dir, 'crop_dir'))
setattr(args, 'xtrain_dir', os.path.join(base_dir, 'xtrain.npy'))
setattr(args, 'ytrain_dir', os.path.join(base_dir, 'ytrain.npy'))
setattr(args, 'xvalid_dir', os.path.join(base_dir, 'xvalid.npy'))
setattr(args, 'yvalid_dir', os.path.join(base_dir, 'yvalid.npy'))
setattr(args, 'xtest_dir', os.path.join(base_dir, 'xtest.npy'))
setattr(args, 'ytest_dir', os.path.join(base_dir, 'ytest.npy'))
setattr(args, 'truey_dir', os.path.join(base_dir, 'truey.npy'))
setattr(args, 'predy_dir', os.path.join(base_dir, 'predy.npy'))
setattr(args, 'checkpoint_path', os.path.join(args.checkpoint_dir, args.name, f'{args.model}.best.hdf5'))


# 데이터가 올 때까지는 scenedetect 부분과 face tracking부분이 필요할 것 같기도 하다 (테스트할 데이터가 없기 때문에)
# send가 온다하더라도 한국버전의 데이터가 필요한데, 굳이 데이터셋이아니더라도 샘플로 보여줄수 있는, 연기 장면도 괜찮음

# 백에 보내줄 때는 프레임별 npy (이미지 벡터 + 감정), 얼굴이 감지된 비디오, 오디오, 오디오 추출, 요약된텍스트와 주요 태그들을 보내주기
# 영상의 파이프라인은 preprocess -> npy화 -> test.py -> npy화가 좋을 것 같음. 이때 라벨의 여부는 신경쓰지 않은 걸로
