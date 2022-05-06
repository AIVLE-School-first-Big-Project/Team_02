import numpy as np
import pandas as pd
import os
import cv2

features = []
labels = []

# labels_data = pd.read_csv('./train_data/train_label1.csv')

# actions = ['0','1','2','3','4','5','6','7','8','9','10','가렵다','개','공원','금요일','내년','내일','냄새나다',
#         '누나','동생','목요일','물','아래','바다','배고프다','병원','불','산','삼키다','선생님','수요일','아빠',
#         '아파트','앞','어제','어지럽다','언니','엄마','오늘','오른쪽','오빠','올해','왼쪽','월요일','위',
#         '음식','일요일','자동차','작년','집','친구','택시','토요일','학교','형','화요일','화장실']
actions = ['가다','감사합니다','괜찮습니다','끝','나','남자','내리다','당신','돕다','맞다',
    '모르다','무엇','미안합니다','반드시','부탁합니다','빨리','수고','수화','슬프다','싫다',
    '아니다','안녕하세요','알다','없다','여자','오다','있다','잘','좋다','주다','키우다','타다'
]

IMAGE_WIDTH = 45
IMAGE_HEIGHT = 80
SEQUENCE_LENGTH = 20

def frames_extraction(video_path):
# Declare a list to store video frames.
    frames_list = []

    cap = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video.
    video_frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the the interval after which frames will be added to the list.
    skip_frames_window = max(int(video_frames_count/SEQUENCE_LENGTH), 1)

    for frame_counter in range(SEQUENCE_LENGTH):

        # Set the current frame position of the video.
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_counter*skip_frames_window)

        # Reading the frame from the video. 
        ret, frame = cap.read()
        if not ret:
            break

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, dsize=(IMAGE_HEIGHT, IMAGE_WIDTH))

        normalized_frame = frame/255
        frames_list.append(normalized_frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(10) == ord('q'):
            break
    
    cap.release()

    return frames_list

for idx_1, word in enumerate(actions):
    VIDEO_FILES = []
    dir_path = f'./train_data/train_video2/{word}'
    for (root, directories, files) in os.walk(dir_path):
        for file in files:
            VIDEO_FILES.append(os.path.join(root, file))

    for idx, video_file in enumerate(VIDEO_FILES):
        frames = frames_extraction(video_file)

        if len(frames) == SEQUENCE_LENGTH:
            features.append(frames)
            labels.append(idx_1)

        print(np.shape(features), actions[idx_1], np.shape(labels))

features = np.array(features)
labels = np.array(labels)

os.makedirs('dataset', exist_ok=True)
np.save(os.path.join('dataset/train_data2_cnn_feature'), features)
np.save(os.path.join('dataset/train_data2_cnn_label'), labels)

cv2.destroyAllWindows()