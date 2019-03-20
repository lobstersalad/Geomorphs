from PIL import Image

img = Image.open('bw_test_dungeon.jpg')
img = img.convert("RGBA")

pixdata = img.load()

width, height = img.size
for y in range(height):
    for x in range(width):
        if pixdata[x, y] == (255, 255, 255, 255):
            pixdata[x, y] = (255, 255, 255, 0)

img.save("transparent_test_dungeon.png", "PNG")

background = Image.open("carpet.jpg")
background = background.resize((1751, 2251))
foreground = Image.open("transparent_test_dungeon.png")

background.paste(foreground, (0, 0), foreground)
background.save("combined.png", "PNG")
