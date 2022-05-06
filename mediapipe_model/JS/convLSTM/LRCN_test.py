import numpy as np
import pandas as pd
import os
import cv2
import tensorflow as tf
from collections import deque

IMAGE_WIDTH = 45
IMAGE_HEIGHT = 80

SEQUENCE_LENGTH = 20

LRCN_model = tf.keras.models.load_model('models/model_cnn_ver02.h5')

CLASSES_LIST = ['0','1','2','3','4','5','6','7','8','9','10','가렵다','개','공원','금요일',
    '내년','내일','냄새나다','누나','동생','목요일','물','아래','바다','배고프다','병원',
    '불','산','삼키다','선생님','수요일','아빠','아파트','앞','어제','어지럽다','언니','엄마',
    '오늘','오른쪽','오빠','올해','왼쪽','월요일','위','음식','일요일','자동차','작년','집',
    '친구','택시','토요일','학교','형','화요일','화장실',
    '가다','감사합니다','괜찮습니다','끝','나','남자','내리다','당신','돕다','맞다',
    '모르다','무엇','미안합니다','반드시','부탁합니다','빨리','수고','수화','슬프다',
    '싫다','아니다','안녕하세요','알다','없다','여자','오다','있다','잘','좋다',
    '주다','키우다','타다'
]

# Initialize the VideoCapture object to read from the video file.
video_reader = cv2.VideoCapture(0)

# Get the width and height of the video.
original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Declare a queue to store video frames.
frames_queue = deque(maxlen = SEQUENCE_LENGTH)

# Initialize a variable to store the predicted action being performed in the video.
predicted_class_name = ''

# Iterate until the video is accessed successfully.
while video_reader.isOpened():

    # Read the frame.
    ok, frame = video_reader.read() 
    
    # Check if frame is not read properly then break the loop.
    if not ok:
        break

    # Resize the Frame to fixed Dimensions.
    resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
    
    # Normalize the resized frame by dividing it with 255 so that each pixel value then lies between 0 and 1.
    normalized_frame = resized_frame / 255

    # Appending the pre-processed frame into the frames list.
    frames_queue.append(normalized_frame)

    # Check if the number of frames in the queue are equal to the fixed sequence length.
    if len(frames_queue) == SEQUENCE_LENGTH:

        # Pass the normalized frames to the model and get the predicted probabilities.
        predicted_labels_probabilities = LRCN_model.predict(np.expand_dims(frames_queue, axis = 0))

        # Get the index of class with highest probability.
        predicted_label = np.argmax(predicted_labels_probabilities)

        # Get the class name using the retrieved index.
        predicted_class_name = CLASSES_LIST[predicted_label]

    # Write predicted class name on top of the frame.
    cv2.imshow('frame', frame)
    print(predicted_class_name)
    # cv2.putText(frame, predicted_class_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
# Release the VideoCapture and VideoWriter objects.
video_reader.release()