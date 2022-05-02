import cv2
import mediapipe as mp
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import statistics
import os
from google.protobuf.json_format import MessageToDict

def meadia_pipe(model, actions):

    os.environ['CUDA_VISIBLE_DEVICES'] = '1'
    os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

    # actions = name
    seq_length = 20

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    seq, action_seq, sentences = [], [], []

    while cap.isOpened():
        _, img = cap.read()

        img = cv2.flip(img, 1)
        img = cv2.resize(img, dsize=(500,500))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if result.multi_hand_landmarks is not None:
            hand_arr = []
            right_hand, left_hand = np.zeros((21,3)), np.zeros((21,3))
            for res in result.multi_hand_landmarks:
                joint = np.zeros((21, 3))
                for j, lm in enumerate(res.landmark):
                    joint[j] = [lm.x, lm.y, lm.z]

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

                handedness_dict = MessageToDict(result.multi_handedness[0])
                if handedness_dict['classification'][0]['label'] == 'Right':
                    right_hand = joint
                else:
                    left_hand = joint


                hand_arr.extend(angle_label)

                mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

            if len(hand_arr) == 15:
                handedness_dict = MessageToDict(result.multi_handedness[0])
                if handedness_dict['classification'][0]['label'] == 'Right':
                    hand_arr = np.concatenate((np.zeros(15), hand_arr))
                else:
                    hand_arr = np.concatenate((hand_arr, np.zeros(15)))
            elif len(hand_arr) > 30:
                continue

            hand_distance = left_hand - right_hand
            hand_distance /= np.linalg.norm(hand_distance, axis=1)[:, np.newaxis]
            hand_arr = np.concatenate((hand_arr, hand_distance.flatten()))
            seq.append(hand_arr)

            if len(seq) < seq_length:
                continue

            input_data = np.expand_dims(np.array(seq[-seq_length:], dtype=np.float32), axis=0)
            y_pred = model.predict(input_data).squeeze()
            i_pred = int(np.argmax(y_pred))
            conf = y_pred[i_pred]
            if conf < 0.8:
                continue

            action = actions[i_pred]
            action_seq.append(action)
            if len(action_seq) < 3:
                continue
            this_action = '?'
            if action_seq[-1] == action_seq[-2] == action_seq[-3]:
                this_action = action
                
            font = ImageFont.truetype("fonts/HMFMMUEX", 40)
            img = Image.fromarray(img)
            draw = ImageDraw.Draw(img)
            draw.text((30,50), this_action, font=font, fill=(255,255,255))
            img = np.array(img)
    
        
        else:
            if len(action_seq) > 0:
                sentences.append(statistics.mode(action_seq))
            action_seq = []

        cv2.imshow('img', img)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            cap.release()
            return sentences
    
# mp_words = meadia_pipe(model1, actions1)
# print(mp_words)    