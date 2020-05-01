import requests
from decouple import config

SECRET_KEY = config('SECRET_KEY')

headers = {
    'Host': 'kakaoi-newtone-openapi.kakao.com',
    'Content-Type': 'application/octet-stream',
    'X-DSS-Service': 'DICTATION',
    'Authorization': f'KakaoAK {SECRET_KEY}',
}

# Transfer-Encoding: chunked # 보내는 양을 모를 땐 이걸 쓴다.

data = open("pansori2.wav", "rb").read()
# print(data)
response = requests.post('https://kakaoi-newtone-openapi.kakao.com/v1/recognize', headers=headers, data=data)
# print(response)
print(response.text)