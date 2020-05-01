import requests
import os
from decouple import config
import json, time

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config('FILE_PATH'))
host_url = config('HOST')
host_model = config('HOST_MODEL')
prod = config('PROD')

def read_from_file():
    with open(file_path, 'r') as f:
        line = f.readline()
        print(line, 'empty:' , line == '')
    return line

def make_request(destination, msg=None, **kwargs):
    if destination == 'model':
        headers = {'Content-Type': 'application/json'}
        response = requests.post(host_url + '/model/invocations', json=msg, headers=headers)
    elif destination == 'api':
        headers = {'Content-Type': 'application/json'}
        post_id = kwargs.get('post_id')
        print(destination, msg)
        response = requests.put(host_url + f'/api/posts/{post_id}/analyze/', json=msg, headers=headers)
    elif destination == 'dequeue':
        response = requests.delete(host_url + '/message')
    elif destination == 'enqueue':
        headers = {'Content-Type': 'application/json'}
        line = kwargs.get('line')
        response = requests.post(host_url + '/message', json=line, headers=headers)
    else:
        response = None
    
    return response


if __name__ == '__main__':
    print('env:', prod)
    while True:
        # read
        line = read_from_file()
        if line == '' or line == None:
            print('no line in queue...')
            time.sleep(5)
            continue

        # request to model
        try:
            line = json.loads(line)
            print('line loaded')
        except:
            print('line status not good')
            new_r = make_request('dequeue')
            print(new_r.status_code, new_r.text)
            time.sleep(1)
            continue
            
        if type(line) == dict and any((line.get('post_id')==None, line.get('user_id')==None, line.get('video_url')==None)):
            print('line status not good')
            new_r = make_request('dequeue')
            print(new_r.status_code, new_r.text)
            time.sleep(1)
            continue
            
        elif type(line) != dict:
            print('line status not good')
            new_r = make_request('dequeue')
            print(new_r.status_code, new_r.text)
            time.sleep(1)
            continue

        post_id = line.get('post_id')

        print('sending message to flask api')

        r = make_request('model', msg=line)
        
        if r.status_code == 200:
            result = r.json()
            print('sending message to backend api')
            new_r = make_request('api', msg=result, post_id=post_id)
            print(new_r.status_code, new_r.text)

            if new_r.status_code != 200:
                print('error with backend')
                new_r = make_request('dequeue')
                # make_request('enqueue', line=line)

            else:
                new_r = make_request('dequeue')
                print(new_r.status_code, new_r.text)
            
            time.sleep(0.5)

        else:
            print(r, r.status_code, r.text)
            time.sleep(0.5)
        
            
