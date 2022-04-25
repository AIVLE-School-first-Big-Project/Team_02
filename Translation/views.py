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

# def braille(text):
#     # 텍스트 to 점자
#     t = Decompose(text)
#     print(t)
#     p = []
#     for s in t:
#         p.append(s[0])
#     return make_img(p)

def textlanguage(request):
    # 수어 to 텍스트... 
    # text = '안녕하세요 2조 여러분'
    # text = '2조 여러분'
    text = '닦달하다 닭다리'
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
    # result_width, result_height = len(arr) * 164, 231
    # crop, turn = 0, 0
    # result = Image.new("L", (result_width, result_height))
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
        
    # for i in range(len(arr)):
    #     if (arr[i] == '') or (i % 3 == 0 and arr[i] =='ㅇ'):
    #         crop += 1
    #         continue
    #     if arr[i] in '0123456789.':
    #         path = f'../Team_02/static/bralille_set/nums/{arr[i]}.png'
    #         turn = 0
    #         continue
        
    #     elif i % 3 == 0:            
    #         path = f'../Team_02/static/bralille_set/chosung/{arr[i]}.png'
    #     elif i % 3 == 1:
    #         path = f'../Team_02/static/bralille_set/joongsung/{arr[i]}.png'
    #     elif i % 3 == 2:
    #         path = f'../Team_02/static/bralille_set/jongsung/{arr[i]}.png'
        # input = Image.open(path)
        # result.paste(im=input, box=(turn*164, 0))
        # turn += 1
    # result = result.crop((0, 0, (len(arr)-crop)*164, 231))
    result = result.resize((int(result.width / 5), int(result.height / 5)))
    filename = time.strftime("%Y%m%d-%H%M%S")
    result.save(f"./static/bralille_translated/{filename}.png")
    context = {'img_path' : filename}
    return JsonResponse(context)