import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('test_dungeon.png')

# Use template matching to find horizontal doors
img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread('doorh_template.png', 0)
# height = .shape[0], width = .shape[1]
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_bw, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
#for pt in zip(*loc[::-1]):
    #cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
#cv2.imwrite('template_matched_doors.png', img)

door = cv2.imread('door.jpg')
map = cv2.imread('textured_combination.png')
#map = img
foreground, background = door.copy(), map.copy()
foreground = cv2.resize(foreground, (int(50), int(50)))

def paste(x, y):
    anchor_y = y
    anchor_x = x

    background_height = background.shape[1]
    background_width = background.shape[1]
    foreground_height = foreground.shape[0]
    foreground_width = foreground.shape[1]

    alpha =1
    # do composite at specified location
    start_y = anchor_y
    start_x = anchor_x
    end_y = anchor_y+foreground_height
    end_x = anchor_x+foreground_width
    blended_portion = cv2.addWeighted(foreground,
                alpha,
                background[start_y:end_y, start_x:end_x,:],
                1 - alpha,
                0,
                background)
    background[start_y:end_y, start_x:end_x,:] = blended_portion

for pt in zip(*loc[::-1]):
    paste(pt[0], pt[1])

cv2.imwrite('textured_doors.png', background)
