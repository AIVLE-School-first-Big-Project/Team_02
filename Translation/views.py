from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index1(request):
    return HttpResponse('<u>Hello</u>') 

# def home(request):
#     return render(request, 'mp/test3.html')    


## ------------------ 웹캠 부분

from tensorflow import keras
from keras.models import load_model
from mp import modeltest # 모델 테스트 함수
from mp import wtsmodel
from mp.models import WToS 

def mp_model(request):

    name = ['0','1','2','3','4','5','6','7','8','9','10','가렵다','개','공원','금요일','내년','내일','냄새나다',
        '누나','동생','수화','물','아래','바다','배고프다','병원','불','산','삼키다','선생님','수요일','아빠',
        '아파트','앞','어제','어지러움','언니','엄마','오늘','오른쪽','오빠','올해','왼쪽','월요일','위에',
        '음식물','일요일','자동차','작년','집','친구','택시','토요일','학교','형','화요일','화장실',
        '가다','감사합니다','괜찮습니다','나','남자','내리다','당신','돕다','맞다',
        '모르다','미안합니다','반드시','부탁합니다','빨리','수고','수화','슬프다','싫다',
        '아니다','안녕하세요','알다','없다','여자','오다','있다','잘','좋다','주다','타다',
        '끝', '무엇', '키우다', '우리', '단체', '번역', '만들다', '사랑합니다', '어디']

    model = load_model("dataset/model_0429_1320.h5")

    mp_words = modeltest.meadia_pipe(model, name)
    
    print(mp_words) 
    #np_words2 = wtsmodel.new_text(mp_words)
    #print(np_words2)

    sentence1 = wtsmodel.predict_mo(mp_words)
    print(sentence1)  

    WToS(text=sentence1).save()

    return render(request, 'mp/test2.html',{ 'data': sentence1 })#, 'text' : WToS.text })

def show(request):
    wtos = WToS.objects.all()
    return render(request, 'mp/test1.html', { 'data': wtos }) 

# -------- 웹 스트리밍 부분 (아직 테스트 중--)
import cv2
import mediapipe as mp
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import statistics
import os
from google.protobuf.json_format import MessageToDict

from django.shortcuts import render
from django.views.decorators import gzip
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
import cv2
from gtts import gTTS
import time
from PIL import Image
import os
from tensorflow import keras
from keras.models import load_model
from Translation import model1_mp, model2_wts # 모델 테스트 함수

from CompoNDecompo.decompose import Decompose
from CompoNDecompo.Alphabets import HEAD_DOUBLE_CONSONANT,TAIL_DOUBLE_CONSONANT
script_dir = os.path.dirname(__file__)
translated_sentence = []
translated_sentence2 = []


import statistics
from google.protobuf.json_format import MessageToDict

translated_sentence = []
action_seq = []
def home(request):
    context = {'data' : translated_sentence}
    
    return render(request, 'mp/test3.html', context)

class VideoCamera(object):
    # global translated_sentence
    def __init__(self): # 초기선언, 환경
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __del__(self):
        self.video.release()
        #cv2.destroyallwindows()
        return 

    # 영상을 jpeg로 인코딩하여, yield로 호출한 URL로 실시간으로 바이너리를 전송
    def get_frame(self, model, actions, seq_length, mp_hands, mp_drawing, hands, seq):
        global translated_sentence
        global action_seq

        ret, image = self.video.read()
        if ret:
            image = cv2.flip(image, 1) 
            result = hands.process(image)

            if result.multi_hand_landmarks is not None:
                hand_arr = []
                right_hand, left_hand = np.zeros((21,3)), np.zeros((21,3))
                for res in result.multi_hand_landmarks:
                    joint = np.zeros((21, 3))
                    for j, lm in enumerate(res.landmark):
                        joint[j] = [lm.x, lm.y, lm.z]

                    v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3] # Parent joint
                    v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3] # Child joint
                    v = v2 - v1 
                    v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
                    angle = np.arccos(np.einsum('nt,nt->n',
                        v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                        v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]
                    angle = np.degrees(angle) # Convert radian to degree
                    angle_label = np.array(angle, dtype=np.float32)
                    handedness_dict = MessageToDict(result.multi_handedness[0])
                    if handedness_dict['classification'][0]['label'] == 'Right':
                        right_hand = joint
                    else:
                        left_hand = joint

                    hand_arr.extend(angle_label)
                    mp_drawing.draw_landmarks(image, res, mp_hands.HAND_CONNECTIONS)

                if len(hand_arr) == 15:
                    handedness_dict = MessageToDict(result.multi_handedness[0])
                    if handedness_dict['classification'][0]['label'] == 'Right':
                        hand_arr = np.concatenate((np.zeros(15), hand_arr))
                    else:
                        hand_arr = np.concatenate((hand_arr, np.zeros(15)))
                elif len(hand_arr) > 30:
                    return None

                hand_distance = left_hand - right_hand
                hand_distance /= np.linalg.norm(hand_distance, axis=1)[:, np.newaxis]
                hand_arr = np.concatenate((hand_arr, hand_distance.flatten()))
                seq.append(hand_arr)

                if len(seq) < seq_length:
                    return None

                input_data = np.expand_dims(np.array(seq[-seq_length:], dtype=np.float32), axis=0)
                y_pred = model.predict(input_data).squeeze()
                i_pred = int(np.argmax(y_pred))
                conf = y_pred[i_pred]
                if conf < 0.8:
                    return None
                    
                action = actions[i_pred]
                action_seq.append(action)

                if len(action_seq) < 3:
                    return None
                this_action = '?'
                if action_seq[-1] == action_seq[-2] == action_seq[-3]:
                    this_action = action

                font = ImageFont.truetype("fonts/gulim.ttc", 40)
                image_pil = Image.fromarray(image)
                draw = ImageDraw.Draw(image_pil)
                draw.text((30,50), this_action, font=font, fill=(1, 1, 1))
                image = np.array(image_pil)

            else:
                if len(action_seq) > 0:
                    translated_sentence.append(statistics.mode(action_seq))
                    action_seq= []

            ret, jpeg =  cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        return None

        # prev_time = 0
        # FPS = 100
        # ret, _ = self.video.read()
        # current_time = time.time() - prev_time

        # if (ret is True) and (current_time > 1./FPS) :
        #     image = self.frame
        #     prev_time = time.time()
        #     _, jpeg = cv2.imencode('.jpg', image)
        #     return jpeg.tobytes()


def gen(camera): # 영상 바이너리 코드를 실시간으로 처리
    model = load_model("dataset/slt_model.h5")
    actions = ['0','1','2','3','4','5','6','7','8','9','10','가렵다','개','공원','금요일','내년','내일','냄새나다',
                '누나','동생','수화','물','아래','바다','배고프다','병원','불','산','삼키다','선생님','수요일','아빠',
                '아파트','앞','어제','어지러움','언니','엄마','오늘','오른쪽','오빠','올해','왼쪽','월요일','위에',
                '음식물','일요일','자동차','작년','집','친구','택시','토요일','학교','형','화요일','화장실',
                '가다','감사합니다','괜찮습니다','나','남자','내리다','당신','돕다','맞다',
                '모르다','미안합니다','반드시','부탁합니다','빨리','수고','수화','슬프다','싫다',
                '아니다','안녕하세요','알다','없다','여자','오다','있다','잘','좋다','주다','타다',
                '끝', '무엇', '키우다', '우리', '단체', '번역', '만들다', '사랑합니다', '어디']
    
    os.environ['CUDA_VISIBLE_DEVICES'] = '1'
    os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
    seq_length = 20

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=2,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5)

    seq = []

    while True:
        frame = camera.get_frame(model, actions, seq_length,  mp_hands, mp_drawing, hands, seq)
        if frame:
            yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # else:
        #     return
    
@gzip.gzip_page
def signlanguage(request):
    global translated_sentence

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

    # name = ['0','1','2','3','4','5','6','7','8','9','10','가렵다','개','공원','금요일','내년','내일','냄새나다',
    #     '누나','동생','수화','물','아래','바다','배고프다','병원','불','산','삼키다','선생님','수요일','아빠',
    #     '아파트','앞','어제','어지러움','언니','엄마','오늘','오른쪽','오빠','올해','왼쪽','월요일','위에',
    #     '음식물','일요일','자동차','작년','집','친구','택시','토요일','학교','형','화요일','화장실',
    #     '가다','감사합니다','괜찮습니다','나','남자','내리다','당신','돕다','맞다',
    #     '모르다','미안합니다','반드시','부탁합니다','빨리','수고','수화','슬프다','싫다',
    #     '아니다','안녕하세요','알다','없다','여자','오다','있다','잘','좋다','주다','타다',
    #     '끝', '무엇', '키우다', '우리', '단체', '번역', '만들다', '사랑합니다', '어디']

    # model = load_model("Translation/file/mp_model.h5")

    # mp_words = model1_mp.meadia_pipe(model, name)
    # print(mp_words)

    # sentence = model2_wts.predict_mo(mp_words)
    # print(sentence)  # 문장 

    # return render(request, '../templates/translation.html',{ 'data': sentence })
    status = request.GET.get('status')
    print('status : ', status)
    print(translated_sentence)
    # return render(request, '../templates/translation.html')   
    return JsonResponse({'data' : translated_sentence})

def textlanguage(request):
    global translated_sentence
    language = request.GET.get('language')
    text = translated_sentence
    # translated_sentence = []
    if language == 'braille':
        text = text.replace(' ', '')
        return braille(text)
    elif language == 'soundlanguage':
        return soundlanguage(text)
    elif language == 'text':
        return JsonResponse({'text' : text})


def soundlanguage(text):
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
    height_num = len(display) // 10 + 1
    result_width, result_height = 10 * 164, 231 * height_num
    result = Image.new("RGBA", (result_width, result_height))
    for idx, b in enumerate(display):
        path = f'../static/bralille_set/{b}.png'
        # input = Image.open(path)
        input = Image.open(os.path.join('../', script_dir, path))
        result.paste(im=input, box=(((idx)%10)*164, (idx // 10) * 231))
    result = result.resize((int(result.width / 7), int(result.height / 7)))
    filename = time.strftime("%Y%m%d-%H%M%S")
    # result.save(f"../static/bralille_translated/{filename}.png")
    save_path = f"../static/bralille_translated/{filename}.png"
    result.save(os.path.join('../', script_dir, save_path))
    context = {'img_path' : filename}
    return JsonResponse(context)


def sts_model(request): # signtosentence_model
    global translated_sentence
    status = request.GET.get('status')
    print('status : ', status)
    # translated_sentence = []
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
    print('sentence: ', sentence)  
    translated_sentence = sentence
    print('translated_sentence: ', translated_sentence)
    # return render(request, '../templates/test111.html',{ 'data': translated_sentence })#, 'text' : WToS.text })
    # return textlanguage(translated_sentence)
    return JsonResponse({'data' : translated_sentence}) 

def textlanguage2(request):
    global translated_sentence2
    translated_sentence2 = request.GET.get('text')
    return JsonResponse({})

def textlanguage2_trans(request):
    global translated_sentence2
    language = request.GET.get('language')
    text = translated_sentence2
    if language == 'braille':
        text = text.replace(' ', '')
        return braille(text)
    elif language == 'soundlanguage':
        return soundlanguage(text)
    elif language == 'signlanguage':
        context = {'img_path' : text}
        return JsonResponse(context)

    try:
        status = request.GET.get('status')
        cam = VideoCamera()
        if status == 'false':
            cam.__del__()       
            return JsonResponse({'data' : translated_sentence })
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("error")
        pass

