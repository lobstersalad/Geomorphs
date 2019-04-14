# Sources: https://stackoverflow.com/questions/8182801/using-imagemagick-to-repeat-or-tile-an-image

import subprocess

# convert blue1.png -roll +0+135 blue_r.png
# montage blue1.png +clone +clone +clone -tile x4 -geometry -1-1 col1.png
# montage blue1_r.png +clone +clone +clone -tile x4 -geometry +0+0 col2.png
# montage -geometry +0+0 col1.png col2.png cols2.png
# convert col2.png -write mpr:tile +delete -size 1920x1080 tile:mpr:tile output.png

# command = ['convert', input + '.png', '-crop', dimensions, '+repage', '+adjoin', output + '_' + dimensions + '_%d.png']
command = []
images = ['blue4.png', 'blue5.png', 'blue6.png', 'blue7.png']
for image in images:
    command.append(image)

command.insert(0, 'montage')

parameters = ['-geometry', '-2-2', 'output.png']
for parameter in parameters:
    command.append(parameter)

# command = ['montage', 'blue1.png', 'blue2.png', 'blue3.png', 'blue4.png', '-geometry', '-1-1', 'output.png']
subprocess.call(command, shell = False)
