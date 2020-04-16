import argparse, os
from datetime import datetime

parser = argparse.ArgumentParser(description="Set configuration for FER model")
parser.add_argument('--timestamp', type=str, default=str(datetime.now().strftime("%Y%m%d%H%M%S")))
parser.add_argument('--name', required=True, type=str)
parser.add_argument('--model', required=True, type=str)
parser.add_argument('--is_data_video', type=str, default='False', help='If data type is video, input True. Model will extract frames and audio')
parser.add_argument('--crop_faces', type=str, default='False', help='If True, model will crop face from dataset')
parser.add_argument('--dataset_path', type=str, default='.\\datasets\\kaggle.csv', help='Path of dataset')
parser.add_argument('--data_dir', type=str, default='.\\data', help='dir path for output of the model')
parser.add_argument('--checkpoint_dir', type=str, default='.\\checkpoints\\train')
parser.add_argument('--from_checkpoint', type=str, default='False')
args = parser.parse_args()