
import matplotlib.pyplot as plt
import numpy as np
import random

def calibration(PDMD, PCamera):
    mCamera = (PCamera[1, 1] - PCamera[1, 0]) / (PCamera[0, 1] - PCamera[0, 0])
    thetaCam = np.arctan(mCamera)
    print thetaCam * 180 / np.pi

    thetaCam = -1 * thetaCam

    rotation = np.array([[np.cos(thetaCam), -np.sin(thetaCam)], [np.sin(thetaCam), np.cos(thetaCam)]])
    PAdjusted = np.matmul(rotation, PCamera)

    Shift = PAdjusted - PDMD
    print Shift
    PAdjusted = PAdjusted - Shift
    return PAdjusted

P1 = np.array([[100, 200], [0, 0]])
plt.close('all')
plt.figure()
plt.scatter(P1[0, :], P1[1, :])
#plt.axis([0, 500, 0, 500])


theta = random.uniform(0, 30) * np.pi / 180
print theta * 180 / np.pi
rotation = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
#print rotation
P2 = np.matmul(rotation, P1)



#plt.scatter(P2[0, :], P2[1, :], color='r')

S = np.array([[random.uniform(-50, 50)], [random.uniform(-50, 50)]])
print S

P3 = P2 + S

plt.scatter(P3[0, :], P3[1, :], color='g')

S2 = P3[:, 0] - P2[:, 0]
S2 = np.transpose(S2)


theta = - theta
rotation = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
P4 = np.matmul(rotation, P3)
#print P4
plt.scatter(P4[0, :], P4[1, :], marker='*', color='k')

S = P1 - P4

P5 = P4 + S

#print P5
plt.scatter(P5[0, :], P5[1, :], marker='*')

###  Calibration!
PDMD = P1

PCamera = P3

PAdjusted = calibration(PDMD, PCamera)


plt.figure()

plt.scatter(PCamera[0, :], PCamera[1, :])
plt.scatter(PDMD[0, :], PDMD[1, :], color='r')
plt.scatter(PAdjusted[0, :], PAdjusted[1, :], color='k', marker='*')
#plt.axis([0, 500, 0, 500])

plt.show()
