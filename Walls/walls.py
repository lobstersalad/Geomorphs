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

# Convert image to gray colourspace
img_bw = cv2.cvtColor(dilated, cv2.COLOR_BGR2GRAY)

# Canny edge detection works very well
tight = cv2.Canny(dilated, 225, 250)
cv2.imwrite('cannytight_test_dungeon.jpg', tight)
wide = cv2.Canny(dilated, 10, 200)
cv2.imwrite('cannywide_test_dungeon.jpg', wide)

# Contours also work well to find edges
(thresh, img_bw) = cv2.threshold(img_bw, 128, 255, 0)
cv2.imwrite('bw_test_dungeon.jpg', img_bw)
contours, hierarchy = cv2.findContours(img_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(dilated, contours, -1, (0, 255, 0), 2)
cv2.imwrite('cnt_test_dungeon.jpg', dilated)

plt.show()
