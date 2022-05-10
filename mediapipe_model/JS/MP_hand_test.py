import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from PIL import ImageFont, ImageDraw, Image
from google.protobuf.json_format import MessageToDict


name = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
    '가렵다', '개', '공원', '금요일', '내년', '내일', '냄새나다',
    '누나', '동생', '목요일', '물', '아래', '바다', '배고프다',
    '병원', '불', '산', '삼키다', '선생님', '수요일', '아빠',
    '아파트', '앞', '어제', '어지럽다', '언니', '엄마', '오늘',
    '오른쪽', '오빠', '올해', '왼쪽', '월요일', '위', '음식',
    '일요일', '자동차', '작년', '집', '친구', '택시', '토요일',
    '학교', '형', '화요일', '화장실', '가다', '감사합니다',
    '괜찮습니다', '끝', '나', '남자', '내리다', '당신', '돕다',
    '맞다', '모르다', '무엇', '미안합니다', '반드시', '부탁합니다',
    '빨리', '수고', '수화', '슬프다', '싫다', '아니다', '안녕하세요',
    '알다', '없다', '여자', '오다', '있다', '잘', '좋다', '주다',
    '키우다', '타다'
    ]

actions = name
seq_length = 10

model = load_model('models/model_xyz_angle.h5')

# MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    model_complexity=0,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


cap = cv2.VideoCapture(0)
zero = np.zeros(78)


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
            joint = np.zeros((21, 3))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            # Compute angles between joints
            v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11,
                        0, 13, 14, 15, 0, 17, 18, 19], :2]  # Parent joint
            v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                        12, 13, 14, 15, 16, 17, 18, 19, 20], :2]  # Child joint
            v = v2 - v1  # [20, 3]
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

            # Get angle using arcos of dot product
            angle = np.arccos(np.einsum(
                'nt,nt->n',
                v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]
                ))  # [15,]

            angle = np.degrees(angle)  # Convert radian to degree

            angle_label = np.array(angle, dtype=np.float32)

            d = np.concatenate([joint.flatten(), angle])
            data_arr.extend(d)
            # data_arr.extend(joint.flatten())

            mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

        if len(data_arr) == 78:
            handedness_dict = MessageToDict(result.multi_handedness[0])
            if handedness_dict['classification'][0]['label'] == 'Right':
                data_arr = np.concatenate((zero, data_arr))
            else:
                data_arr = np.concatenate((data_arr, zero))
        elif len(data_arr) > 156:
            continue

        seq.append(data_arr)

        if len(seq) < seq_length:
            continue

        input_data = np.expand_dims(np.array(seq[-seq_length:],
                                             dtype=np.float32), axis=0)
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

        font = ImageFont.truetype("fonts/gulim.ttc", 20)
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        draw.text((30, 50), this_action, font=font, fill=(0, 0, 255))
        img = np.array(img)

    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
