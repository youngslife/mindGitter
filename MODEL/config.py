import argparse, os
from datetime import datetime

parser = argparse.ArgumentParser(description="Set configuration for FER model")
parser.add_argument('--timestamp', type=str, default=str(datetime.now().strftime("%Y%m%d%H%M%S")))
parser.add_argument('--name', required=True, type=str, help='The unit of project. Name folder under data will be created to store outcomes when you run models.')
parser.add_argument('--model', required=True, type=str, help='The model you want to use to face emotion recognition. There is only sCNN now.')
parser.add_argument('--is_train', type=str, default='True', help='If want to run test, it should be False')
parser.add_argument('--is_data_video', type=str, default='False', help='If data type is video, input True. Model will extract frames and audio')
parser.add_argument('--crop_faces', type=str, default='False', help='If True, model will crop face from dataset')
parser.add_argument('--dataset_path', type=str, default='.\\datasets\\kaggle.csv', help='Path of dataset')
parser.add_argument('--data_dir', type=str, default='.\\data', help='dir path for output of the model')
parser.add_argument('--checkpoint_dir', type=str, default='.\\checkpoints', help='Base dir of Checkpoints. According to Options checkpoints_path will be created. e.g.checkpoints/name/train')
parser.add_argument('--from_checkpoint', type=str, default='False', help='Input True if want to train from the checkpoints')
args = parser.parse_args()

base_dir = os.path.join(args.data_dir, args.name)
setattr(args, 'xtrain_dir', os.path.join(base_dir, 'xtrain.npy'))
setattr(args, 'ytrain_dir', os.path.join(base_dir, 'ytrain.npy'))
setattr(args, 'xvalid_dir', os.path.join(base_dir, 'xvalid.npy'))
setattr(args, 'yvalid_dir', os.path.join(base_dir, 'yvalid.npy'))
setattr(args, 'xtest_dir', os.path.join(base_dir, 'xtest.npy'))
setattr(args, 'ytest_dir', os.path.join(base_dir, 'ytest.npy'))
setattr(args, 'checkpoint_path', os.path.join(args.checkpoint_dir, args.name, f'{args.model}.best.hdf5'))