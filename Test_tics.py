import Tkinter
import tkFileDialog
from PIL import Image
import matplotlib.image as mpimg
from scipy import optimize
from pylab import *


def func_cyto(x, *p):
    return p[1] * 1.0/(1 + x / p[0]) + p[2]

def func_int(x, *p):
    return p[1] * exp(-x / p[0]) + p[2]


if __name__ == "__main__":
    ti = 1  # time per frame in seconds

    root = Tkinter.Tk()
    root.withdraw()

    # Retrieving sequence of images
    #file_path = tkFileDialog.askopenfilename()
    file_path = 'sequence.tiff'
    #print(file_path)

    tiffStack = Image.open(file_path)
    tiffStack.load()
    nbImTot = tiffStack.n_frames
    #print(tiffStack.n_frames)

    '''
    tiffStack.seek(0)
    img = np.asarray(tiffStack, dtype='int8')
    print(type(img))
    print(tiffStack.size)
    figure()
    plt.imshow(img, cmap='gray')
    
    
    img2 = mpimg.imread(file_path)
    print(type(img2))
    figure()
    plt.imshow(img2, cmap='gray')
    plt.show()
    '''

    arrayShape = tiffStack.size + (nbImTot, )
    #print(arrayShape)
    I = np.zeros(arrayShape)

    for i in range(nbImTot):
        tiffStack.seek(i)
        I[:, :, i] = np.asarray(tiffStack)
        #figure()
        #plt.imshow(I[:, :, i], cmap='gray')

    #plt.show()
    #print(I.shape)

    # Retrieving background
    file_path = 'background.tiff'
    tiffStack = Image.open(file_path)
    tiffStack.load()
    nbImBck = tiffStack.n_frames
    arrayShape = tiffStack.size + (nbImBck, )
    Bkg = np.zeros(arrayShape)

    for i in range(nbImBck):
        tiffStack.seek(i)
        Bkg[:, :, i] = np.asarray(tiffStack)

    print(Bkg.shape)

    backgrd = np.mean(Bkg)
    Icorr = I-backgrd

    Imoy = mean(I, axis=2)
    Icorrmoy = mean(Icorr, axis=2)

    figure()
    plt.subplot(2, 1, 1)
    plt.imshow(Imoy, cmap='gray')
    plt.title("Average of {:d} Images".format(nbImTot))
    plt.colorbar()
    plt.subplot(2, 1, 2)
    plt.imshow(Icorrmoy, cmap='gray')
    plt.title('After background substraction')
    plt.colorbar()
    NbIm = nbImTot

    AC = zeros(NbIm)
    for i in range(NbIm):
        a = np.zeros(NbIm-i)
        for j in range(NbIm-i-1):
            temp = Icorr[:, :, j]
            Imoyj = np.mean(temp)
            #print(temp)
            temp2 = Icorr[:, :, j+i]
            Imoyd = np.mean(temp2)
            #print(Imoyd)
            dI = temp.reshape(-1) - Imoyj
            dI_d = temp2.reshape(-1) - Imoyd
            a[j] = np.mean(dI * dI_d)/(Imoyj * Imoyd)
        AC[i] = np.sum(a)/(NbIm - i)

    tau = np.arange(1, NbIm) * ti
    print(tau.shape)
    print(AC[1:].shape)
    figure()
    plt.plot(tau, AC[1:])
    plt.title("Autocorrelation")


    # Fit
    # Cyto

    xdata = np.arange(1, int(np.round(NbIm*0.5))) * ti
    ydata = AC[1: int(np.round(NbIm*0.5))]
    # parameters:tauD,g0,ginf
    pInit = [1, 0.1, 0.1]
    lb = [0.5, 0.00001, 0]
    ub = [500, 10, 1]

    pop, pcov = optimize.curve_fit(func_cyto, xdata, ydata,
                                   p0=pInit, bounds=(lb, ub))
    print (pop)

    yfit = func_cyto(xdata, *pop)
    tauD = pop[0]
    print(tauD)
    g0 = pop[1]
    ginf = pop[2]
    print(ginf)
    Nmob = g0 / ((ginf + g0) ** 2)
    print(Nmob)
    immo = ginf / (ginf + g0)
    print(immo*100)
    plt.plot(xdata, yfit, 'r--')

    # Interaction model

    popi, picov = optimize.curve_fit(func_int, xdata, ydata,
                                     p0=pInit, bounds=(lb, ub))
    print (popi)

    yfiti = func_int(xdata, *popi)

    toff = popi[0]
    print(toff)
    g0i = popi[1]
    ginfi = popi[2]
    print(ginfi)
    Nmobi = g0i / ((ginfi + g0i) ** 2)
    print(Nmob)
    immoi = ginfi / (ginfi + g0i)
    print(immoi * 100)
    plt.plot(xdata, yfiti, 'g--')
    plt.show()