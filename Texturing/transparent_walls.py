# Sources: https://stackoverflow.com/questions/36921496/how-to-join-png-with-alpha-transparency-in-a-frame-in-realtime

import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image

img = Image.open('cnt_test_dungeon.png')
img = img.convert("RGBA")

pixdata = img.load()

width, height = img.size
for y in range(height):
    for x in range(width):
        if pixdata[x, y] != (0, 0, 0, 255) and pixdata[x, y] != (255, 255, 255, 255):
            pixdata[x, y] = (0, 255, 0, 0)

img.save("transparent_walls_dungeon.png", "PNG")

# ...or OpenCV
dungeon = cv2.imread("carpet.jpg", -1)
dungeon = cv2.resize(dungeon, (int(1751), int(2251)))
overlay = cv2.imread("transparent_walls_dungeon.png", -1) # Load with transparency

overlay_img = overlay[:,:,:3] # Grab the BRG planes
overlay_mask = overlay[:,:,3:]  # And the alpha plane

# Again calculate the inverse mask
background_mask = 255 - overlay_mask

# Turn the masks into three channel, so we can use them as weights
overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

# Create a masked out face image, and masked out overlay
# We convert the images to floating point in range 0.0 - 1.0
#dungeon = dungeon[..., np.newaxis] for adding singleton dimension
#dungeon = np.squeeze(dungeon) to remove all singleton dimensions
dungeon_part = (dungeon * (1 / 255.0)) * (background_mask * (1 / 255.0))
overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

# And finally just add them together, and rescale it back to an 8bit integer image
result = np.uint8(cv2.addWeighted(dungeon_part, 255.0, overlay_part, 255.0, 0.0))
cv2.imwrite("textured_walls_transparency.png", result)
