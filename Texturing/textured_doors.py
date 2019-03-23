import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('test_dungeon.png')

# Use template matching to find horizontal doors
img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread('doorh_template.png', 0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_bw, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    print(pt)
cv2.imwrite('AAAAA.png', img)

b = loc[loc][:, 0].argsort()]
grp_idx = np.flatnonzero(np.r_[True, (b[:-1, 0] != b[1:, 0])])
grp_maxY = np.maximum.reduceat(b[:, 1], grp_idx)
