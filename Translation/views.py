from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, JsonResponse
import cv2
import threading
from gtts import gTTS
import time

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
    # 아마 모델링 코드...? 텍스트를 넘겨준다
    context = {}
    text = '2조화이팅'
    context['text'] = text
    context['audio_path'] = soundlanguage(text)
    context['braille_path'] = braille(text)
    # {'filename' : f"{filename}"}
    try:
        cam = VideoCamera()
        JsonResponse(context)
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("error")
        pass

    
def braille(request):
    # 텍스트 to 점자
    print("braille")
    return

def textlanguage(request):
    # 수어 to 텍스트... 
    print("textlanguage")
    return

# def soundlanguage(request):
#     # 텍스트 to 음성
#     text = '안녕하세요'
#     tts = gTTS(text=text, lang='ko')
#     filename = time.strftime("%Y%m%d-%H%M%S")
#     tts.save(f"./static/audio/{filename}.mp3")
#     return render(request, 'Translation/test.html', {'filename' : f"{filename}"})

def soundlanguage(text):
    # 텍스트 to 음성
    tts = gTTS(text=text, lang='ko')
    filename = time.strftime("%Y%m%d-%H%M%S")
    tts.save(f"./static/audio/{filename}.mp3")
    return filename