# This python code uses MicroManager device drivers to control a camera. 
# Tested on Hamamatsu Orca Flash 4 camera, should work similarly on other cameras.
# Original idea: Kay Schink @koschink
# Gist implementation: Nikita Vladimirov @nvladimus

#Environment setup instructions: https://micro-manager.org/wiki/Using_the_Micro-Manager_python_library
import sys
sys.path.append("C:\\Program Files\\Micro-Manager-1.4")
import MMCorePy #load MicroManager for device control
import matplotlib.pyplot as plt

#load camera and set it up
mmc = MMCorePy.CMMCore()
mmc.getVersionInfo()
mmc.loadDevice('Camera', 'DemoCamera', 'DCam')
mmc.initializeAllDevices()
mmc.setCameraDevice('Camera')

#Optional block: set an output trigger for synchronization with other devices
#mmc.getDevicePropertyNames('Camera') #execute if forgot prop names
#mmc.getProperty('Camera','OUTPUT TRIGGER PERIOD UNITS') #seconds
#mmc.getAllowedPropertyValues('Camera','OUTPUT TRIGGER KIND[0]') #check what's allowed
#mmc.setProperty('Camera','OUTPUT TRIGGER KIND[0]','PROGRAMABLE')
#mmc.setProperty('Camera','OUTPUT TRIGGER PERIOD[0]',0.001)
#mmc.setProperty('Camera','OUTPUT TRIGGER POLARITY[0]','POSITIVE')

mmc.setExposure(20) #ms
mmc.snapImage()
img = mmc.getImage() #this is numpy array, by the way
plt.imshow(img, cmap='gray')
plt.show()
# pretty image should be displayed here

mmc.reset() #say good byemicromanager.py 