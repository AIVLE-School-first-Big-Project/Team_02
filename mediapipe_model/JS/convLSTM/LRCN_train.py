import numpy as np
import pandas as pd
import os
import cv2

data = pd.read_csv('mp_data/train_label1.csv')
labels = data['label']

X = []
Y = []
image_width = 450
image_height = 800

VIDEO_FILES = []
dir_path = 'mp_data/train_video2'
for (root, directories, files) in os.walk(dir_path):
    for file in files:
        VIDEO_FILES.append(os.path.join(root, file))

for idx, file in enumerate(VIDEO_FILES):
    cap = cv2.VideoCapture(file)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, None, fx=image_width/frame.shape[1], fy=image_height/frame.shape[0])
        X.append(frame/255)
        Y.append(labels[idx])
        # cv2.imshow('frame', frame)
    print(np.shape(X), np.shape(Y))

X = np.array(X)
Y = np.array(Y)
X = X.reshape((X.shape), 1)
# print(X.shape, Y.shape)
np.save(os.path.join('dataset/train_data1_cnn_X'), X)
np.save(os.path.join('dataset/train_data1_cnn_Y'), Y)

cap.release()
cv2.destroyAllWindows()