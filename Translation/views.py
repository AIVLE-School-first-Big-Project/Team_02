from django.shortcuts import render
from django.views.decorators import gzip
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
import cv2
import threading
from gtts import gTTS
import time
from PIL import Image
import os

from CompoNDecompo.decompose import Decompose
from CompoNDecompo.Alphabets import HEAD_DOUBLE_CONSONANT,TAIL_DOUBLE_CONSONANT
script_dir = os.path.dirname(__file__)

def home(request):
    context = {}
    return render(request, '../templates/translation.html', context)

class VideoCamera(object):

    def __init__(self):
        # 웹캠 켜짐
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        print(1)
        # 프레임 추출
        # (self.grabbed, self.frame) = self.video.read()
        # 실시간 영상을 위해 스레드 구현
        # threading.Thread(target=self.update, args=()).start()
        
    # 카메라 정지
    def __del__(self):
        self.video.release()
        return

    # 영상을 jpg 바이너리로 변환하여 리턴
    def get_frame(self):
        # image = self.frame
        # retval, jpeg = cv2.imencode('.jpg', image)
        ret, image = self.video.read()
        if ret:
            ret, jpeg =  cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        return None

            

    # 프레임 추출
    # def update(self):
    #     while True:
    #         (self.grabbed, self.frame) = self.video.read()
    #         if any([self.grabbed, self.frame]):
    #             break

    
# def gen(camera):
#     frame = camera.get_frame()
#     yield(b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            return


@gzip.gzip_page
def signlanguage(request):
    # try:
    #     status = request.GET.get('status')
    #     cam = VideoCamera()
    #     if status == 'false':
    #         cam.__del__()
    #         return JsonResponse({})
    #     return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    # except:
    #     print("error")
    #     pass

    name = ['0','1','2','3','4','5','6','7','8','9','10','가렵다','개','공원','금요일','내년','내일','냄새나다',
        '누나','동생','수화','물','아래','바다','배고프다','병원','불','산','삼키다','선생님','수요일','아빠',
        '아파트','앞','어제','어지러움','언니','엄마','오늘','오른쪽','오빠','올해','왼쪽','월요일','위에',
        '음식물','일요일','자동차','작년','집','친구','택시','토요일','학교','형','화요일','화장실',
        '가다','감사합니다','괜찮습니다','나','남자','내리다','당신','돕다','맞다',
        '모르다','미안합니다','반드시','부탁합니다','빨리','수고','수화','슬프다','싫다',
        '아니다','안녕하세요','알다','없다','여자','오다','있다','잘','좋다','주다','타다',
        '끝', '무엇', '키우다', '우리', '단체', '번역', '만들다', '사랑합니다', '어디']

    model = load_model("Translation/file/mp_model.h5")

    mp_words = model1_mp.meadia_pipe(model, name)
    print(mp_words)

    sentence = model2_wts.predict_mo(mp_words)
    print(sentence)  # 문장 

    return render(request, '../templates/translation.html',{ 'data': sentence })


def textlanguage(request):
    # 수어 to 텍스트... 
    text = '수화 번역을 만들었습니다'
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
    tts.save(os.path.join('../', script_dir, f"../static/audio/{filename}.mp3"))
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
        path = f'../static/bralille_set/{b}.png'
        # input = Image.open(path)
        input = Image.open(os.path.join('../', script_dir, path))
        result.paste(im=input, box=(idx*164, 0))
    result = result.resize((int(result.width / 7), int(result.height / 7)))
    filename = time.strftime("%Y%m%d-%H%M%S")
    # result.save(f"../static/bralille_translated/{filename}.png")
    save_path = f"../static/bralille_translated/{filename}.png"
    result.save(os.path.join('../', script_dir, save_path))
    context = {'img_path' : filename}
    return JsonResponse(context)

<<<<<<< HEAD

=======
from tensorflow import keras
from keras.models import load_model
from Translation import model1_mp, model2_wts # 모델 테스트 함수

def sts_model(request): # signtosentence_model

    name = ['0','1','2','3','4','5','6','7','8','9','10','가렵다','개','공원','금요일','내년','내일','냄새나다',
        '누나','동생','수화','물','아래','바다','배고프다','병원','불','산','삼키다','선생님','수요일','아빠',
        '아파트','앞','어제','어지러움','언니','엄마','오늘','오른쪽','오빠','올해','왼쪽','월요일','위에',
        '음식물','일요일','자동차','작년','집','친구','택시','토요일','학교','형','화요일','화장실',
        '가다','감사합니다','괜찮습니다','나','남자','내리다','당신','돕다','맞다',
        '모르다','미안합니다','반드시','부탁합니다','빨리','수고','수화','슬프다','싫다',
        '아니다','안녕하세요','알다','없다','여자','오다','있다','잘','좋다','주다','타다',
        '끝', '무엇', '키우다', '우리', '단체', '번역', '만들다', '사랑합니다', '어디']

    model = load_model("Translation/file/mp_model.h5")

    mp_words = model1_mp.meadia_pipe(model, name)
    print(mp_words) 

    sentence = model2_wts.predict_mo(mp_words)
    print(sentence)  

    return render(request, '../templates/test111.html',{ 'data': sentence })#, 'text' : WToS.text })
>>>>>>> 4460c6a303ec7755bcf8353aedc3680e7e809c03
