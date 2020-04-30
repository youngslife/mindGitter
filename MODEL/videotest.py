import os, subprocess, cv2, glob, pickle
command = ("ffmpeg -y -i %s -qscale:v 2 -async 1 -r 10 %s" % ('https://mind-gitter-diary.s3.ap-northeast-2.amazonaws.com/diary/11587947625451.mp4', 'video.avi'))
output = subprocess.call(command, stdout=None)
# command = ("ffmpeg -y -i %s -qscale:v 2 -threads 1 -f image2 %s" % 'https://mind-gitter-diary.s3.ap-northeast-2.amazonaws.com/diary/11587946672480.mp4', os.path.join('testsss/','%06d.jpg')) 
# output = subprocess.call(command, stdout=None)
command = ("ffmpeg -y -i %s -ac 1 -vn -acodec pcm_s16le -ar 16000 %s" % ('https://mind-gitter-diary.s3.ap-northeast-2.amazonaws.com/diary/11587947625451.mp4', 'audio.wav')) 
output = subprocess.call(command, stdout=None) # ar 은 frame과 상관이있나?