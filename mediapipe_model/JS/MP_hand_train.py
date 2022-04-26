import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os
from google.protobuf.json_format import MessageToDict

data = pd.read_csv('mp_data/label.csv', encoding='euc-kr')

actions = data['label']

# LSTM Window Size
seq_length = 10

VIDEO_FILES = []
dir_path = 'mp_data/0001~3000/'
for (root, directories, files) in os.walk(dir_path):
    for file in files:
        VIDEO_FILES.append(os.path.join(root, file))

# MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    model_complexity=1,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7)

os.makedirs('dataset', exist_ok=True)
zero = np.zeros(99) 

for idx, file in enumerate(VIDEO_FILES):
    cap = cv2.VideoCapture(file)
    action = actions[idx]
    data = []

    while cap.isOpened():

        ret, img = cap.read()
        if not ret:
            break

        img = cv2.flip(img, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if result.multi_hand_landmarks:
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

                angle_label = np.array(angle, dtype=np.float32)
                # angle_label = np.append(angle_label, idx)

                d = np.concatenate([joint.flatten(), angle_label])

                mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)
            
                data_arr.extend(d)
               
            if len(data_arr) == 99:
                handedness_dict = MessageToDict(result.multi_handedness[0])
                if handedness_dict['classification'][0]['label'] == 'Right':
                    data_arr = np.concatenate((zero, data_arr))
                else:
                    data_arr = np.concatenate((data_arr, zero))
            elif len(data_arr) > 198:
                continue
            data_arr = np.append(data_arr, idx)
            data.append(data_arr)
            
        cv2.imshow('img', img)
        if cv2.waitKey(1) == ord('q'):
            break
    
    data = np.array(data)
    print(action, data.shape)
    
    if len(data) < seq_length:
        continue
    # np.save(os.path.join('dataset', f'raw_{action}'), data)

    # Create sequence data
    try:
        full_seq_data = []
        for seq in range(len(data) - seq_length):
            full_seq_data.append(data[seq:seq + seq_length])
        full_seq_data = np.array(full_seq_data)
        print(action, full_seq_data.shape)
        
        if idx == 0:
            full_data = full_seq_data
            continue
        
        full_data = np.concatenate((full_data, full_seq_data))
        print(action, full_data.shape)
        # np.save(os.path.join('dataset', f'seq_{action}'), full_seq_data)
    
    except:
        print('ERROR!!', action, idx)
        pass

cv2.destroyAllWindows()
cap.release()

np.save(os.path.join('dataset/full_data'), full_data)