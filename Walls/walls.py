# Sources: https://opencv-python-tutroals.readthedocs.io
#          https://stackoverflow.com/questions/30757273/opencv-findcontours-complains-if-used-with-black-white-image
#          https://stackoverflow.com/questions/51171028/find-the-perimeter-of-the-leaf

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('test_dungeon.jpg')

# Dilating image will remove small grid lines, doors, other artefacts
kernel = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(img, kernel, iterations = 2)
cv2.imwrite('dilated_test_dungeon.jpg', dilated)

# Convert dilated image to gray colourspace
dilated_bw = cv2.cvtColor(dilated, cv2.COLOR_BGR2GRAY)

# Canny edge detection works very well
tight = cv2.Canny(dilated, 225, 250)
cv2.imwrite('cannytight_test_dungeon.jpg', tight)
wide = cv2.Canny(dilated, 10, 200)
cv2.imwrite('cannywide_test_dungeon.jpg', wide)

# Contours also work well to find edges
(thresh, dilated_bw) = cv2.threshold(dilated_bw, 128, 255, 0)
cv2.imwrite('bw_test_dungeon.jpg', dilated_bw)
contours, hierarchy = cv2.findContours(dilated_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(dilated, contours, -1, (0, 255, 0), 2)
cv2.imwrite('cnt_test_dungeon.jpg', dilated)

# Use template matching to find "doors" on original image
img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread('doorh_template.png', 0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_bw, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('test_dungeon_doors.jpg', img)
