'''
Simple script used to plot annoation for synthesized images
'''
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import skimage.io

def readjoint(filename):
    with open(filename) as f:
        pts = []
        for l in f:
            fs = l.split(',')
            name = fs[0]; x = int(fs[1]); y = int(fs[2])
            pts.append(dict(name = name, x = x, y = y))
    return pts


# def update(fid):
#     '''
#     API here: http://matplotlib.org/api/animation_api.html
#     '''
#     print('Update %d' % fid)
#     fid += 1
#     pts = readjoint('./joint/%04d.csv' % fid)
#     im = skimage.io.imread('./video/%04d.png' % fid)
#     plt.imshow(im)
#     for pt in pts:
#         plt.plot(pt['x'], pt['y'], '*')
#         print(pt)

fig = plt.figure()

fid = 1
pts = readjoint('./joint/%04d.csv' % fid)
im = skimage.io.imread('./video/%04d.png' % fid)
plt.imshow(im)
for pt in pts:
    plt.plot(pt['x'], pt['y'], '*')
    print(pt)

# ani = animation.FuncAnimation(fig, update, 25,
#     interval=50, blit=True)
plt.show()

