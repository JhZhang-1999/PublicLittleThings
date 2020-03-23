import random
import cv2
import numpy as np

img = np.zeros((500, 500, 3), np.uint8)

shapeorg = []
for i in range(15):
    shapeorg.append(random.randrange(0,2))

shape = [0]*25
shape[:15]=shapeorg
for i in range(15,20):
    shape[i] = shape[i-10]
for i in range(20,25):
    shape[i] = shape[i-20]

col = []
for i in range(3):
    col.append(random.randrange(0,256))

pos = []
for i in [0,100,200,300,400]:
    for j in [0,100,200,300,400]:
        pos.append((i,j))

# 左上顶点，右下顶点
for i in range(len(pos)):
    if shape[i] == 1:
        cv2.rectangle(img, pos[i], (pos[i][0]+100,pos[i][1]+100), col, thickness=-1)
    else:
        cv2.rectangle(img, pos[i], (pos[i][0]+100,pos[i][1]+100), (240,240,240), thickness=-1)

cv2.imshow('1',img)
cv2.waitKey()