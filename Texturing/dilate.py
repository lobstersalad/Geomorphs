import cv2
import numpy as np
from matplotlib import pyplot as plt

# Read image into variable
img = cv2.imread('transparent_test_dungeon.png')

# Dilating image will remove small grid lines, doors, other artefacts
kernel = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(img, kernel, iterations = 1)
cv2.imwrite('dilated_test_dungeon.png', dilated)
