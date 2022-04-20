from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, JsonResponse
import cv2
import threading
from gtts import gTTS
import time

from CompoNDecompo.decompose import Decompose


def home(request):
    context = {}
    return render(request, 'Translation/translation1 copy.html', context)

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def signlanguage(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("error")
        pass

def braille(text):
    # 텍스트 to 점자
    t=Decompose(text)
    p = []
    for s in t:
        p.append(s[0])
    return make_img(p)

def textlanguage(request):
    # 수어 to 텍스트... 
    text = '이조 화이팅'
    language = request.GET.get('language')
    if language == 'braille':
        text = text.replace(' ', '')
        return braille(text)
    elif language == 'soundlanguage':
        return soundlanguage(text)

def soundlanguage(text):
    # 텍스트 to 음성
    tts = gTTS(text=text, lang='ko')
    filename = time.strftime("%Y%m%d-%H%M%S")
    tts.save(f"./static/audio/{filename}.mp3")
    context = {'audio_path' : filename}
    return JsonResponse(context)

from PIL import Image
def make_img(arr):
    blank = arr.count('')
    result_width = (len(arr)-blank) * 164
    result_height = 231
    result = Image.new("RGB", (result_width, result_height))
    turn = 0
    for i in range(len(arr)):
        if arr[i] == '':
            continue
        if i % 3 == 0:
            path = f'../Team_02/static/bralille_set/chosung/{arr[i]}.png'
        elif i % 3 == 1:
            path = f'../Team_02/static/bralille_set/joongsung/{arr[i]}.png'
        elif i % 3 == 2:
            path = f'../Team_02/static/bralille_set/jongsung/{arr[i]}.png'
        input = Image.open(path)
        result.paste(im=input, box=(turn*164, 0))
        turn += 1
    result = result.resize((int(result.width / 5), int(result.height / 5)))
    # result.show()
    filename = time.strftime("%Y%m%d-%H%M%S")
    result.save(f"./static/bralille_translated/{filename}.png")
    context = {'img_path' : filename}
    return JsonResponse(context)
