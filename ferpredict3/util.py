import time, json, io, urllib
from boto3 import client
from boto3.s3.transfer import S3Transfer

from decouple import config
import logging, boto3, os, requests
from botocore.exceptions import ClientError

def upload_file(file_name, form, end, bucket):
    ACCESS_KEY_ID = config('ACCESS_KEY_ID')
    ACCESS_SECRET_KEY = config('ACCESS_SECRET_KEY')
    credentials = {
      'aws_access_key_id':ACCESS_KEY_ID,
      'aws_secret_access_key':ACCESS_SECRET_KEY
    }
    object_name = 'emotions/' + form["user_id"] + form["post_id"] + end

    # Upload the file
    s3_client = client('s3', **credentials)
    transfer = S3Transfer(s3_client)
    try:
        transfer.upload_file(file_name, bucket, object_name, extra_args={'ACL': 'public-read-write'})

    except ClientError as e:
        logging.error(e)
        return False
    return object_name


def speaking_to_text(filename, form):
  ACCESS_KEY_ID = config('ACCESS_KEY_ID')
  ACCESS_SECRET_KEY = config('ACCESS_SECRET_KEY')
  transcribe = boto3.client('transcribe', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_SECRET_KEY, region_name='ap-northeast-2')
  job_name = "transcribe_"+form["user_id"]+"_"+form["post_id"]
  job_uri = "https://mind-gitter-diary.s3.ap-northeast-2.amazonaws.com/"+filename
  transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='wav',
    LanguageCode='ko-KR'
  )
  while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
      break
    print('Still dictation work')
    time.sleep(2)
  if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
    response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
    data = json.loads(response.read())
    text = data['results']['transcripts'][0]['transcript']
    sents = text.split('. ')
    return sents, text

