import os
import cv2
import time
import statistics
import mediapipe as mp
import numpy as np
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators import gzip
from PIL import ImageFont, ImageDraw, Image
from google.protobuf.json_format import MessageToDict
from gtts import gTTS
from keras.models import load_model
from Translation import model_wts # 모델 테스트 함수
from CompoNDecompo.decompose import Decompose

script_dir = os.path.dirname(__file__)
translated_sentence = []
action_seq = []
translated_sentence2 = []


def home(request):
    context = {'data' : translated_sentence}
    
    return render(request, '../templates/translation.html', context)

def textlanguage(request):
    global translated_sentence
    language = request.GET.get('language')
    text = translated_sentence
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
        input = Image.open(os.path.join('../', script_dir, path))
        result.paste(im=input, box=(((idx)%10)*164, (idx // 10) * 231))
    result = result.resize((int(result.width / 7), int(result.height / 7)))
    filename = time.strftime("%Y%m%d-%H%M%S")
    save_path = f"../static/bralille_translated/{filename}.png"
    result.save(os.path.join('../', script_dir, save_path))
    context = {'img_path' : filename}
    return JsonResponse(context) 

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


# 웹 스트리밍 부분 -- 


class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        
    # 카메라 정지
    def __del__(self):
        self.video.release()
        return

    # 영상을 jpg 바이너리로 변환하여 리턴
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

def gen(camera):
    model = load_model("Translation/file/mp_model.h5")
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
    try:
        status = request.GET.get('status')
        cam = VideoCamera()
        if status == 'false':
            cam.__del__()       
            sentence = model_wts.predict_mo(translated_sentence)
            translated_sentence = sentence
            return JsonResponse({'data' : sentence })
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("error")
        pass

