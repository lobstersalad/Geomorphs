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
 - Resize original image to very large before any processing happens
    - Need to resize template images and retune dilation for this to work
    - Might produce better quality map for tiled floors
 - Template matching for wall segments
'''

import random
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import os
from os import listdir, walk
from os.path import isfile, join

def texture(final_path, texture_path, floor_type, tiling):
    # Find array of x, y coordinates for given special tile type
    def match(template, image):
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.98
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
    wall_texture = cv2.imread('../Textures/Untiled/tiles.png', -1)
    if tiling == False:
        if floor_type == "Grass":
            floor_texture = cv2.imread('../Textures/Untiled/grass.png', -1)
        else:
            floor_texture = cv2.imread('../Textures/Untiled/tiles.png', -1)

    #  Dilate and draw contours
    # ------------------------------------------------------------------------------
    print ('Drawing Walls...')
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(original, kernel, iterations = 2)
    dilated = cv2.cvtColor(dilated, cv2.COLOR_BGR2GRAY)
    (thresh, dilated) = cv2.threshold(dilated, 128, 255, 0)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    dilated = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(dilated, contours, -1, (0, 255, 0), 10)

    # Texture walls
    # ------------------------------------------------------------------------------
    print ('Texturing Walls...')
    textured_walls = Image.fromarray(dilated)
    textured_walls = textured_walls.convert('RGBA')
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
    print ('Texturing Floor...')
    if tiling == False:
        textured_walls = cv2.cvtColor(textured_walls, cv2.COLOR_BGRA2RGBA)
        textured_combination = Image.fromarray(textured_walls)
        textured_combination = textured_combination.convert('RGBA')
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
        path = '../Templates/Tiles/'
        floor_tile_templates = [file for file in listdir(path) if isfile(join(path, file))]
        rotation = [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]
        textured_combination = textured_walls
        background = textured_walls
        if floor_type == "Brown":
            tile_path = '../Textures/Brown_Tiles/'
        elif floor_type == "Cave":
            tile_path = '../Textures/Cave_Tiles/'
        elif floor_type == "Runes":
            tile_path = '../Textures/Runes_Tiles/'
        elif floor_type == "White":
            tile_path = '../Textures/White_Tiles/'
        tile_count = len(next(os.walk(path)))
        for template in floor_tile_templates:
            tile_template = cv2.imread(path + template, 0)
            loc = match(tile_template, original_bw)
            for pt in zip(*loc[::-1]):
                foreground = cv2.imread(tile_path + 'tile' + str(random.randint(1, tile_count)) + '.png', -1)
                foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
                degrees = random.randint(0, 3)
                if (degrees != 3):
                    foreground = cv2.rotate(foreground, rotation[degrees])
                foreground = cv2.resize(foreground, (int(51), int(51)))
                paste(pt[0], pt[1])

        #loc = match(tile_template, original_bw)

    # Texture Special Tiles
    # Doors
    # ------------------------------------------------------------------------------
    print ('Texturing Special Tiles...')
    background = textured_combination
    #foreground = cv2.resize(foreground, (int(51), int(51)))

    path = '../Templates/Doors/Horizontal/'
    horizontal_door_templates = [file for file in listdir(path) if isfile(join(path, file))]
    for template in horizontal_door_templates:
        door_template = cv2.imread(path + template, 0)
        loc = match(door_template, original_bw)
        foreground = cv2.imread('../Textures/Doors/doorh_small.png', -1)
        foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
        for pt in zip(*loc[::-1]):
            paste(pt[0], pt[1] + 18)

    path = '../Templates/Doors/Vertical/'
    vertical_door_templates = [file for file in listdir(path) if isfile(join(path, file))]
    for template in vertical_door_templates:
        door_template = cv2.imread(path + template, 0)
        loc = match(door_template, original_bw)
        foreground = cv2.imread('../Textures/Doors/doorv_small.png', -1)
        foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
        for pt in zip(*loc[::-1]):
            paste(pt[0] + 18, pt[1])

    # Stairs
    # ------------------------------------------------------------------------------
    temp = cv2.imread('../Templates/Stairs/stairs_pointdown.png', 0)
    loc = match(temp, original_bw)
    foreground = cv2.imread('../Textures/Stairs/stairsv.png', -1)
    foreground = cv2.rotate(foreground, cv2.ROTATE_180)
    foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
    for pt in zip(*loc[::-1]):
        paste(pt[0], pt[1])

    temp = cv2.imread('../Templates/Stairs/stairs_pointleft.png', 0)
    loc = match(temp, original_bw)
    foreground = cv2.imread('../Textures/Stairs/stairsh.png', -1)
    foreground = cv2.rotate(foreground, cv2.ROTATE_180)
    foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
    for pt in zip(*loc[::-1]):
        paste(pt[0], pt[1])

    temp = cv2.imread('../Templates/Stairs/stairs_pointright.png', 0)
    loc = match(temp, original_bw)
    foreground = cv2.imread('../Textures/Stairs/stairsh.png', -1)
    foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
    for pt in zip(*loc[::-1]):
        paste(pt[0], pt[1])

    temp = cv2.imread('../Templates/Stairs/stairs_pointup.png', 0)
    loc = match(temp, original_bw)
    foreground = cv2.imread('../Textures/Stairs/stairsv.png', -1)
    foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
    for pt in zip(*loc[::-1]):
        paste(pt[0], pt[1])

    temp = cv2.imread('../Templates/Stairs/stairs_opendown.png', 0)
    loc = match(temp, original_bw)
    foreground = cv2.imread('../Textures/Stairs/stairsv.png', -1)
    foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
    for pt in zip(*loc[::-1]):
        paste(pt[0], pt[1])

    temp = cv2.imread('../Templates/Stairs/stairs_openleft.png', 0)
    loc = match(temp, original_bw)
    foreground = cv2.imread('../Textures/Stairs/stairsh.png', -1)
    foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
    for pt in zip(*loc[::-1]):
        paste(pt[0], pt[1])

    temp = cv2.imread('../Templates/Stairs/stairs_openright.png', 0)
    loc = match(temp, original_bw)
    foreground = cv2.imread('../Textures/Stairs/stairsh.png', -1)
    foreground = cv2.rotate(foreground, cv2.ROTATE_180)
    foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
    for pt in zip(*loc[::-1]):
        paste(pt[0], pt[1])

    temp = cv2.imread('../Templates/Stairs/stairs_openup.png', 0)
    loc = match(temp, original_bw)
    foreground = cv2.imread('../Textures/Stairs/stairsv.png', -1)
    foreground = cv2.rotate(foreground, cv2.ROTATE_180)
    foreground = cv2.cvtColor(foreground, cv2.COLOR_BGRA2BGR)
    for pt in zip(*loc[::-1]):
        paste(pt[0], pt[1])

    # Final image
    cv2.imwrite(final_path, background)

if __name__ == 'texture':
    texture()
