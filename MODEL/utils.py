import os
import config
from datetime import datetime

def save_logs():
  args = vars(config.args)
  args_values = ",".join([str(i) for i in args.values()]) + '\n'
  logs_dir = '.\\logs.txt'
  with open(logs_dir, 'a') as logs:
    logs.write(args_values)
  print(f'configs are saved at logs.txt')