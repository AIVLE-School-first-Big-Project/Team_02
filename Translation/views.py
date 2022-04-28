from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, JsonResponse
import cv2
import threading
from gtts import gTTS
import time
from PIL import Image

from CompoNDecompo.decompose import Decompose
from CompoNDecompo.Alphabets import HEAD_DOUBLE_CONSONANT,TAIL_DOUBLE_CONSONANT

def home(request):
    context = {}
    return render(request, '../templates/translation.html', context)

class VideoCamera(object):

    def __init__(self):
        # 웹캠 켜짐
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # 프레임 추출
        (self.grabbed, self.frame) = self.video.read()
        # 실시간 영상을 위해 스레드 구현
        threading.Thread(target=self.update, args=()).start()
        
    # 카메라 정지
    def __del__(self):
        self.video.release()

    # 영상을 jpg 바이너리로 변환하여 리턴
    def get_frame(self):
        try:
            image = self.frame
            retval, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        except:
            cap = cv2.VideoCapture(0)
            cap.release()
            return
            

    # 프레임 추출
    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            if any([self.grabbed, self.frame]):
                break

def delcam():
    cap = cv2.VideoCapture(0)
    cap.release()
    return 
    
def gen(camera):
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


def textlanguage(request):
    # 수어 to 텍스트... 
    text = '안녕하세요 2조 여러분'
    # text = '2조 여러분'
    # text = '닦달하다 닭다리'
    # text = '아 이'
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

def braille(text):
    arr = Decompose(text)
    dict = {0:'chosung', 1:'joongsung', 2:'jongsung'}
    display = []
    for word in arr:
        for idx, syllable in enumerate(word):
            if (syllable == '') or (idx == 0 and syllable =='ㅇ'):
                continue
            elif syllable in '0123456789.':
                display.append(f'nums/{syllable}')
            else:
                display.append(f'{dict[idx%3]}/{syllable}')
    result_width, result_height = len(display) * 164, 231
    result = Image.new("L", (result_width, result_height))
    for idx, b in enumerate(display):
        path = f'../Team_02/static/bralille_set/{b}.png'
        input = Image.open(path)
        result.paste(im=input, box=(idx*164, 0))
    result = result.resize((int(result.width / 5), int(result.height / 5)))
    filename = time.strftime("%Y%m%d-%H%M%S")
    result.save(f"./static/bralille_translated/{filename}.png")
    context = {'img_path' : filename}
    return JsonResponse(context)