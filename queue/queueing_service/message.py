import os
from flask import Flask, request
from decouple import config
import json

app = Flask(__name__)

try:
    prefix = config('ROUTES')
except:
    print(' *** prefix not defined.')
    prefix = ''

print(' *** Routes:', prefix)

class MsgController(object):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config('FILE_PATH'))

    @classmethod
    def create(cls):
        print('trying to create file in', cls.file_path)
        # create file
        with open(cls.file_path, 'w') as f:
            print('made file')

        return cls.check_exists()

    @classmethod
    def check_exists(cls):
        return os.path.isfile(cls.file_path)

    @classmethod
    def enqueue(cls, message):
        # append to file with message
        with open(cls.file_path, 'a') as f:
            f.write(json.dumps(message))
            f.write('\n')
        return True

    @classmethod
    def dequeue(cls):
        # delete first line from file
        with open(cls.file_path, 'r+') as f:
            new_f = f.readlines()
            if len(new_f) > 0: del new_f[0]
            f.seek(0)
            for line in new_f:
                f.write(line)
            f.truncate()

        return len(new_f)

@app.route(prefix + '/status')
def hello():
    return 'good'

@app.route(prefix + '/', methods=['POST'])
def add_msg():
    count = 0
    while True:
        count += 1
        if MsgController.check_exists():
            break
        elif count > 10:
            return 'Error: No file exists' # 500
        else:
            res = MsgController.create()
            if res == True: break
    
    data = request.get_json()
    MsgController.enqueue(data)

    return 'Done'

@app.route(prefix + '/', methods=['DELETE'])
def delete_msg():
    result = MsgController.dequeue()
    return str(result)
