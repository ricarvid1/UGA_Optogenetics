'''
from pylab import *
ion()

import MMCorePy
mmc = MMCorePy.CMMCore()
mmc.loadDevice("cam","DemoCamera","DCam")
mmc.initializeDevice("cam")

print "Test acquire and display of monochrome images."

figure()
mmc.setCameraDevice("cam")
mmc.snapImage()
im1 = mmc.getImage()
imshow(im1,cmap = cm.gray)
'''

''' MICRO MANAGER TUTORIAL '''


#First steps
#Adding micro manager to the sys path
import sys
sys.path.append("C:\\Program Files\\Micro-Manager-1.4")


import MMCorePy
mmc = MMCorePy.CMMCore()  # Instance micromanager core
mmc.getVersionInfo()
mmc.getAPIVersionInfo()

#First steps
#Demo camera
mmc.loadDevice('Camera', 'DemoCamera', 'DCam')
#Hamamatsu
#mmc.loadDevice('Camera', 'HamamatsuHam', 'HamamatsuHam_DCAM')
mmc.initializeAllDevices()
mmc.setCameraDevice('Camera')

#Snapping single image
mmc.snapImage()

img = mmc.getImage()  # img - it's just numpy array
img

#plotting image
from pylab import *
ion()
import matplotlib.pyplot as plt
#grayscale
plt.close()
figure()
plt.imshow(img, cmap='gray')
plt.show()  # And window will appear

#acquiring image color   
'''
mmc.setProperty('Camera', 'PixelType', '32bitRGB')  # Change pixel type
mmc.snapImage()
rgb32 = mmc.getImage()
rgb32

#Numpy array         
import numpy as np
rgb32.shape
rgb = rgb32.view(dtype=np.uint8).reshape(
           rgb32.shape[0], rgb32.shape[1], 4)[...,2::-1]
rgb.shape
rgb.dtype

figure()
plt.imshow(rgb32)
'''

mmc.reset()