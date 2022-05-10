import cv2
import mediapipe as mp
import numpy as np
import os
from google.protobuf.json_format import MessageToDict

actions = [
    '가다', '감사합니다', '괜찮습니다', '나', '남자',
    '내리다', '당신', '돕다', '맞다', '모르다', '미안합니다',
    '반드시', '부탁합니다', '빨리', '수고', '수화', '슬프다',
    '싫다', '아니다', '안녕하세요', '알다', '없다', '여자',
    '오다', '있다', '잘', '좋다', '주다', '타다'
    ]

# LSTM Window Size
seq_length = 10

# MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    model_complexity=0,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

os.makedirs('dataset', exist_ok=True)
zero = np.zeros(78)

for idx_1, action in enumerate(actions):
    VIDEO_FILES = []
    dir_path = f'mp_data/train_video2/{action}'
    for (root, directories, files) in os.walk(dir_path):
        for file in files:
            VIDEO_FILES.append(os.path.join(root, file))

    for idx, file in enumerate(VIDEO_FILES):
        cap = cv2.VideoCapture(file)
        data = []

        while cap.isOpened():

            ret, img = cap.read()
            try:
                img = img[0:800, :]
                img = cv2.resize(img, (800, 450))

            except Exception as e:
                print(str(e))
            if not ret:
                break

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = hands.process(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            if result.multi_hand_landmarks:
                data_arr = []
                for res in result.multi_hand_landmarks:
                    joint = np.zeros((21, 3))
                    for j, lm in enumerate(res.landmark):
                        joint[j] = [lm.x, lm.y, lm.z]

                    # Compute angles between joints
                    # Parent joint
                    v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10,
                                11, 0, 13, 14, 15, 0, 17, 18, 19], :2]
                    # Child joint
                    v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :2]
                    v = v2 - v1  # [20, 3]
                    # Normalize v
                    v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                    # Get angle using arcos of dot product
                    angle = np.arccos(np.einsum(
                        'nt,nt->n',
                        v[[0, 1, 2, 4, 5, 6, 8, 9, 10,
                           12, 13, 14, 16, 17, 18], :],
                        v[[1, 2, 3, 5, 6, 7, 9, 10, 11,
                           13, 14, 15, 17, 18, 19], :]))  # [15,]

                    angle = np.degrees(angle)  # Convert radian to degree

                    angle_label = np.array(angle, dtype=np.float32)

                    d = np.concatenate([joint.flatten(), angle_label])

                    mp_drawing.draw_landmarks(img, res,
                                              mp_hands.HAND_CONNECTIONS)

                    data_arr.extend(d)

                if len(data_arr) == 78:
                    handedness_dict = MessageToDict(result.multi_handedness[0])
                    if handedness_dict['classification'][0]['label'] == 'Right':
                        data_arr = np.concatenate((zero, data_arr))
                    else:
                        data_arr = np.concatenate((data_arr, zero))
                elif len(data_arr) > 156:
                    continue
                data_arr = np.append(data_arr, idx_1+57)
                data.append(data_arr)

            cv2.imshow('img', img)
            if cv2.waitKey(1) == ord('q'):
                break

        data = np.array(data)
        print(action, data.shape)

        if len(data) < seq_length:
            continue

        # Create sequence data
        try:
            full_seq_data = []
            for seq in range(len(data) - seq_length):
                full_seq_data.append(data[seq:seq + seq_length])
            full_seq_data = np.array(full_seq_data)
            print(action, full_seq_data.shape)

            if idx_1 == 0 and idx == 0:
                full_data = full_seq_data
                continue

            full_data = np.concatenate((full_data, full_seq_data))
            print(action, full_data.shape)

        except Exception:
            print('ERROR!!', action, idx)
            pass

cv2.destroyAllWindows()
cap.release()

np.save(os.path.join('dataset/train_data2_win10_ver03'), full_data)
