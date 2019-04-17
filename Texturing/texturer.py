# Sources: https://opencv-python-tutroals.readthedocs.io
#          https://stackoverflow.com/questions/30757273/opencv-findcontours-complains-if-used-with-black-white-image
#          https://stackoverflow.com/questions/36921496/how-to-join-png-with-alpha-transparency-in-a-frame-in-realtime
#          https://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent

'''
Procedure
1. Template matching for special tiles, save locations
2. Dilate
3. Draw contours
4. Transparency layering for floor (optional) and walls
5. Paste in special tiles
'''

'''
ToDo
 - Count number of files in tile directories for RNG tiling
 - Add images for all door types and numbered tiles
 - Resize original image to very large before any processing happens
    - Need to resize template images and retune dilation for this to work
    - Might produce better quality map for tiled floors
 - Template matching for wall segments
'''

'''
Bugs
 - ? Fixed - Some dungeon layouts with doors give a difference of array size / channel error, has been hard to reproduce
             but has something to do with special tile locations
'''
import random
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

def texture(texture_path, tiling):
    # Find array of x, y coordinates for given special tile type
    def match(template, image):
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.90
        loc = np.where( res >= threshold)
        return loc

    # Apply special tile textures to pre-determined locations
    def paste(x, y):
        anchor_x = x
        anchor_y = y

        background_width = background.shape[1]
        background_height = background.shape[0]
        foreground_width = foreground.shape[1]
        foreground_height = foreground.shape[0]

        alpha = 1
        start_x = anchor_x
        start_y = anchor_y
        end_x = anchor_x+foreground_width
        end_y = anchor_y+foreground_height
        blended_portion = cv2.addWeighted(foreground,
                    alpha,
                    background[start_y:end_y, start_x:end_x,:],
                    1 - alpha,
                    0,
                    background)
        background[start_y:end_y, start_x:end_x,:] = blended_portion

    # Load required images into variables
    # ------------------------------------------------------------------------------
    original = cv2.imread(texture_path, -1)
    original_bw = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    doorh_template = cv2.imread('../Templates/doorh_template.png', 0)
    doorv_template = cv2.imread('../Templates/doorv_template.png', 0)
    door_texture = cv2.imread('../Textures/Doors/door1.png', -1)
    wall_texture = cv2.imread('../Textures/Testing/tiles.png', -1)
    floor_texture = cv2.imread('../Textures/Testing/grass.png', -1)

    #  Dilate and draw contours
    # ------------------------------------------------------------------------------
    print ("Drawing Walls...")
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(original, kernel, iterations = 2)
    dilated = cv2.cvtColor(dilated, cv2.COLOR_BGR2GRAY)
    (thresh, dilated) = cv2.threshold(dilated, 128, 255, 0)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    dilated = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(dilated, contours, -1, (0, 255, 0), 10)

    # Texture walls
    # ------------------------------------------------------------------------------
    print ("Texturing Walls...")
    textured_walls = Image.fromarray(dilated)
    textured_walls = textured_walls.convert("RGBA")
    data = textured_walls.load()

    # Convert all pixels within contour lines to transparent
    width, height = textured_walls.size
    for y in range(height):
        for x in range(width):
            if data[x, y] != (0, 0, 0, 255) and data[x, y] != (255, 255, 255, 255):
                data[x, y] = (0, 255, 0, 0)

    wall_texture = cv2.resize(wall_texture, (int(original.shape[1]), int(original.shape[0])))
    textured_walls = cv2.cvtColor(np.array(textured_walls), cv2.COLOR_RGBA2BGRA)

    # Separate RGB and Alpha channels, apply texture to Alpha portion, recombine
    textured_walls_img = textured_walls[:,:,:3]
    textured_walls_mask = textured_walls[:,:,3:]
    background_mask = 255 - textured_walls_mask
    textured_walls_mask = cv2.cvtColor(textured_walls_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)
    wall_texture_part = (wall_texture * (1 / 255.0)) * (background_mask * (1 / 255.0))
    textured_walls_part = (textured_walls_img * (1 / 255.0)) * (textured_walls_mask * (1 / 255.0))
    textured_walls = np.uint8(cv2.addWeighted(wall_texture_part, 255.0, textured_walls_part, 255.0, 0.0))

    # Texture floor
    # ------------------------------------------------------------------------------
    print ("Texturing Floor...")
    if tiling == False:
        textured_walls = cv2.cvtColor(textured_walls, cv2.COLOR_BGRA2RGBA)
        textured_combination = Image.fromarray(textured_walls)
        textured_combination = textured_combination.convert("RGBA")
        data = textured_combination.load()

        # Convert all non-transparent white pixels to transparent
        width, height = textured_combination.size
        for y in range(height):
            for x in range(width):
                if data[x, y] == (255, 255, 255, 255):
                    data[x, y] = (255, 255, 255, 0)

        floor_texture = cv2.resize(floor_texture, (int(original.shape[1]), int(original.shape[0])))
        textured_combination = cv2.cvtColor(np.array(textured_combination), cv2.COLOR_RGBA2BGRA)

        # Separate RGB and Alpha channels, apply texture to Alpha portion, recombine
        textured_combination_img = textured_combination[:,:,:3]
        textured_combination_mask = textured_combination[:,:,3:]
        background_mask = 255 - textured_combination_mask
        textured_combination_mask = cv2.cvtColor(textured_combination_mask, cv2.COLOR_GRAY2BGR)
        background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)
        floor_texture_part = (floor_texture * (1 / 255.0)) * (background_mask * (1 / 255.0))
        textured_combination_part = (textured_combination_img * (1 / 255.0)) * (textured_combination_mask * (1 / 255.0))
        textured_combination = np.uint8(cv2.addWeighted(floor_texture_part, 255.0, textured_combination_part, 255.0, 0.0))
    else:
        tile_template = cv2.imread('../Templates/tile_template.png', 0)
        textured_combination = textured_walls
        background = textured_walls
        rotation = [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]

        loc = match(tile_template, original_bw)
        for pt in zip(*loc[::-1]):
            foreground = cv2.imread('../Textures/White_Tiles/tile' + str(random.randint(1, 34)) + '.png', -1)
            degrees = random.randint(0, 3)
            if (degrees != 3):
                foreground = cv2.rotate(foreground, rotation[degrees])
            foreground = cv2.resize(foreground, (int(51), int(51)))
            paste(pt[0], pt[1])

    # Texture special tiles
    # ------------------------------------------------------------------------------
    print ("Texturing Special Tiles...")
    foreground, background = door_texture, textured_combination
    foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
    foreground = cv2.resize(foreground, (int(51), int(51)))

    loc = match(doorh_template, original_bw)
    for pt in zip(*loc[::-1]):
        paste(pt[0], pt[1])

    loc = match(doorv_template, original_bw)
    for pt in zip(*loc[::-1]):
        paste(pt[0], pt[1])

    # Final image
    cv2.imwrite('../Texturing/textured_dungeon.png', background)
    print ("Finished!")

if __name__ == "texture":
    texture()
