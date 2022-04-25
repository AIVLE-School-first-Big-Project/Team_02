import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from PIL import ImageFont, ImageDraw, Image
from google.protobuf.json_format import MessageToDict

num = [str(n) for n in range(101)]

name = ['112','119','1000','10000',
    '가렵다','가스','가슴','가시','각목','갇히다','감금','감전','강','강남구','강동구',
    '강북구','강서구','강풍','개','거실','걸렸다','결박','경운기','경찰','경찰차','계곡',
    '계단','고속도로','고압전선','고열','고장','부러지다','골절','탈골','곰','공사장',
    '공원','놀이터','공장','관악구','광진구','교통사고','구급대','구급대원','구급차',
    '구로구','구청','구해주세요','귀','금가다','금요일','금천구','급류','기절','기절하다',
    '깔리다','끓는물','남자친구','남편','남학생','납치','낫','낯선남자','낯선사람','낯선여자',
    '내년','내일','냄새나다','노원구','논','농약','누나','누수','누전','누출','눈','다리',
    '다음','달(월)','대문앞','도둑','절도','도로','도봉구','독극물','독버섯','독사','동대문구',
    '동생','동작구','동전','두드러기생기다','뒤','뒤통수','등','딸','떨어지다','쓰러지다',
    '뜨거운물','마당','마포구','말려주세요','말벌','맹견','머리','멧돼지','목','목요일',
    '무너지다','붕괴','무릎','문틈','물','밑에','아래','바다','반점생기다','발','발가락',
    '발목','발작','방망이','밭','배','복부','배고프다','뱀','벌','범람','벼락','병원',
    '보건소','보내주세요(경찰)','보내주세요(구급차)','복통','볼','부엌','불','불나다','붕대',
    '비닐하우스','비상약','빌라','뼈','사이','산','살충제','살해','삼키다','서대문구','서랍',
    '서울시','서초구','선반','선생님','성동구','성북구','성폭행','소방관','소방차','소화기',
    '소화전','손','손가락','손목','송파구','수영장','수요일','술취한 사람','숨을안쉬다','시청',
    '신고하세요(경찰)','심장마비','아기','아이들','어린이','아내','아들','아빠','아저씨','아줌마',
    '아파트','인대','안방','알려주세요','앞','앞집','약국','약사','양천구','어깨','어제',
    '어지러움','언니','얼굴','엄마','엘리베이터','여자친구','여학생','연기','연락해주세요','열',
    '열나다','열어주세요','엽총','영등포구','옆집','옆집 아저씨','옆집 할아버지','옆집사람','옆쪽',
    '오늘','오른쪽','오른쪽-귀','오른쪽-눈','오빠','옥상','올해','왼쪽','왼쪽-귀','왼쪽-눈',
    '욕실','용산구','우리집','운동장','월요일','위','위에','위협','윗집','윗집사람','유리',
    '유치원','유치원 버스','은평구','음식물','응급대원','응급처리','의사','이마','이물질','이번',
    '이상한사람','이웃집','일요일','임산부','임신한아내','자동차','자살','자상','작년','작은방',
    '장난감','장단지','절단','제초제','조난','종로구','주','중구','중랑구','지난','지혈대','진통제',
    '질식','집','집단폭행','차밖','차안','창문','창백하다','체온계','총','추락','축사','출산',
    '출혈','피나다','친구','침수','칼','코','택시','토요일','토하다','통학버스','트랙터','트럭',
    '파도','파편','팔','팔꿈치','폭발','폭탄','폭우','폭행','학교','학생','할머니','할아버지',
    '함몰되다','해(연)','해독제','해열제','허리','허벅지','현관','현관앞','협박','형','호흡곤란',
    '호흡기','홍수','화상','화약','화요일','화장실','화재'
]

name = num+name

actions = name
# actions = ['a', 'b']
# seq_length = 30
seq_length = 10

model = load_model('models/model_3.h5')

# MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    model_complexity = 0,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


cap = cv2.VideoCapture('mp_data/0001~3000/KETI_SL_0000000120.avi')
zero = np.zeros(99)

# w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# out = cv2.VideoWriter('input.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), (w, h))
# out2 = cv2.VideoWriter('output.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), (w, h))

seq = []
action_seq = []

while cap.isOpened():
    ret, img = cap.read()
    img0 = img.copy()

    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks is not None:
        data_arr = []
        for res in result.multi_hand_landmarks:
            joint = np.zeros((21, 4))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z, lm.visibility]

            # Compute angles between joints
            v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3] # Parent joint
            v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3] # Child joint
            v = v2 - v1 # [20, 3]
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

            # Get angle using arcos of dot product
            angle = np.arccos(np.einsum('nt,nt->n',
                v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

            angle = np.degrees(angle) # Convert radian to degree

            d = np.concatenate([joint.flatten(), angle])
            data_arr.extend(d)

            mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)
            
        if len(data_arr) == 99:
            handedness_dict = MessageToDict(result.multi_handedness[0])
            if handedness_dict['classification'][0]['label'] == 'Right':
                data_arr = np.concatenate((zero, data_arr))
            else:
                data_arr = np.concatenate((data_arr, zero))
        elif len(data_arr) > 198:
            continue
            
        seq.append(data_arr)
        
        if len(seq) < seq_length:
            continue
            
        input_data = np.expand_dims(np.array(seq[-seq_length:], dtype=np.float32), axis=0)
        y_pred = model.predict(input_data).squeeze()
        i_pred = int(np.argmax(y_pred))
        conf = y_pred[i_pred]
        
        if conf < 0.7:
            continue
            
        
        action = actions[i_pred]
        print(action)
        action_seq.append(action)
        if len(action_seq) < 3:
            continue
        this_action = '?'
        if action_seq[-1] == action_seq[-2] == action_seq[-3]:
            this_action = action
            
        # cv2.putText(img, f'{this_action.upper()}', org=(int(res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0] + 20)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
        font = ImageFont.truetype("fonts/gulim.ttc", 20)
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        draw.text((30,50), this_action, font=font, fill=(0,0,255))
        img = np.array(img)

    # out.write(img0)
    # out2.write(img)
    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break
    
cv2.destroyAllWindows()
cap.release()