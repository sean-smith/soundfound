# File: audioUtilities.py
# Author: Wayne Snyder
# Date: 4/26/15
# Purpose: This collects together the most important algorithms used in
#          CS 591, in order to work interactively; for the most part
#          signals are manipulated as arrays, not as wave files.
#          This file assumes you have scipy and numpy.

import array
import contextlib
import wave
import math
import cmath 
import numpy as np
import matplotlib.pyplot as plt
from numpy import pi
#from scipy.io.wavfile import read, write
#from scipy import signal
#from numpy.random import randint

# Basic parameters

numChannels   = 1                      # mono
sampleWidth   = 2                      # in bytes, a 16-bit short
SR            = 44100                  #  sample rate
MAX_AMP       = (2**(8*sampleWidth - 1) - 1)    #maximum amplitude is 2**15 - 1  = 32767
MIN_AMP       = -(2**(8*sampleWidth - 1))       #min amp is -2**15
windowWidth   = 4410
windowSlide   = 2205


# File I/O  

# Read a wave file and return the entire file as a standard array

def readWaveFile(infile,withParams=False,asNumpy=False):
    with contextlib.closing(wave.open(infile)) as f:
        params = f.getparams()
        frames = f.readframes(params[3])
        print(params)
        if(params[0] != 1):
            print("Warning in reading file: must be a mono file!")
        if(params[1] != 2):
            print("Warning in reading file: must be 16-bit sample type!")
        if(params[2] != 44100):
            print("Warning in reading file: must be 44100 sample rate!")
    if asNumpy:
        X = np.array(frames,dtype='int16')
    else:  
        X = array.array('h', frames)
    if withParams:
        return X,params
    else:
        return X
         
def spectrumFFT(X):
    S = []
    R = np.fft.rfft(X)
    WR = 44100/len(X)
    for i in range(len(R)):
        S.append( ( i*WR, 2.0 * np.absolute(R[i])/len(X),np.angle(R[i]) ))
    return S


def graphSpectrum(X):
    S = spectrumFFT(X)
    # print(S)
    F = []
    s_1 = []
    for f,s,h in S:
        F += [f]
        s_1 += [s]
    plt.plot(F,s_1)
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")

    x_max = max(S, key=lambda x: x[1])[0]
    print (x_max)
    plt.axis([0.0,x_max*1.2, 0,MAX_AMP])
    ax = plt.gca()
    ax.set_autoscale_on(False)

    plt.show()



# Write an array X; since the wave library can not deal with
# numpy arrays, we have to convert it just in case

def writeWaveFile(fname, X):
    X = [int(x) for x in X]
    params = [1,2, SR , len(X), "NONE", None]
    X = [int(x) for x in X]
    data = array.array("h",X)
    with contextlib.closing(wave.open(fname, "w")) as f:
        f.setparams(params)
        f.writeframes(data.tobytes())
    print(fname + " written.")
    


# round to 4 decimal places

def round4(x):
    return round(x+0.00000000001,4)

"""    
Display a signal with various options

   xUnits are scale of x axis: "Seconds" (default), "Milliseconds", or "Samples"
   yUnits are "Relative" [-1..1] (default) or "Absolute" [-MAX_AMP-1 .. MAX_AMP])
   left and right delimit range of signal displayed: [left .. right) in xUnits
   width is width of figure (height is 3)


"""

def displaySignal(X, left = 0, right = -1, xUnits = "Seconds", yUnits = "Relative",width=10):

        
    minAmplitude = -(2**15 + 100)        # just to improve visibility of curve
    maxAmplitude = 2**15 + 300    
    
    if(xUnits == "Sample"):
        if(right == -1):
            right = len(X)
        T = range(left,right)
        Y = X[left:right]
    elif(xUnits == "Seconds"):
        if(right == -1):
            right = len(X)/44100
        T = np.arange(left, right, 1/44100)
        leftSampleNum = int(left*44100)
        Y = X[leftSampleNum:(leftSampleNum + len(T))]
    elif(xUnits == "Milliseconds"):
        if(right == -1):
            right = len(X)/44.1
        T = np.arange(left, right, 1/44.1)
        leftSampleNum = int(left*44.1)
        Y = X[leftSampleNum:(leftSampleNum + len(T))]
    else:
        print("Illegal value for xUnits")
        
    if(yUnits == "Relative"):
        minAmplitude = -1.003            # just to improve visibility of curve
        maxAmplitude = 1.01
        Y = [x/32767 for x in Y]

    fig = plt.figure(figsize=(width,3))   # Set x and y dimensions of window: may need to redo for your display
    fig.suptitle('Signal Window for X', fontsize=14, fontweight='bold')
    ax = plt.axes()
    ax.set_xlabel(xUnits)
    ax.set_ylabel(yUnits + ' Amplitude')
    ax.set_ylim([minAmplitude,maxAmplitude])
    ax.set_xlim([left, right])
    plt.axhline(0, color='black')      # draw the 0 line in black
    plt.plot(T,Y) 
    if(    (xUnits == "Samples" and (right - left) < 44)
        or (xUnits == "Seconds" and (right - left) < 0.001)
        or (xUnits == "Milliseconds" and (right - left) < 1) ):
            plt.plot(T,Y, 'bo')                     
    plt.grid(True)                     # if you want dotted grid lines
    plt.show()
    
""" 
#    If want to use interactive window, type
#         #matplotlib qt
#    to console; to get back to inline mode, type
#         #matplotlib inline
#    to console; then use following in place of plt.show()
    
    mngr = plt.get_current_fig_manager()
    geom = mngr.window.geometry()
    x,y,dx,dy = geom.getRect()
    mngr.window.setGeometry(0, 0, dx, dy)
    plt.show()
    fig.canvas.manager.window.raise_()
"""
    
    

  
# some useful spectra    

def makeSpectrum(instr,freq=1):
    if(instr=="clarinet"):
        return [(freq,0.314,0.0), 
        (freq*3,.236,0.0), 
        (freq*5,0.157,0.0), 
        (freq*7,0.044,0.0), 
        (freq*9,0.157,0.0), 
        (freq*11,0.038,0.0), 
        (freq*13,0.053,0.0)]  
    elif(instr=="bell"):
        return [(freq,0.1666,0.0), 
        (freq*2,0.1666,0.0), 
        (freq*3,0.1666,0.0), 
        (freq*4.2,0.1666,0.0), 
        (freq*5.4,0.1666,0.0), 
        (freq*6.8,0.1666,0.0)]  
    elif(instr=="steelstring"):
        return [(freq*0.7272, .00278,0.0),
                (freq, .0598,0.0),
                (freq*2, .2554,0.0),
                (freq*3, .0685,0.0),
                (freq*4, .0029,0.0),
                (freq*5, .0126,0.0),
                (freq*6, .0154,0.0),
                (freq*7, .0066,0.0),
                (freq*8, .0033,0.0),
                (freq*11.0455, .0029,0.0),
                (freq*12.0455, .0094,0.0),
                (freq*13.0455, .0010,0.0),
                (freq*14.0455, .0106,0.0),
                (freq*15.0455, .0038,0.0)]
    else:
        return []


    
# return a window by slicing a signal delimited by [begin..end) in seconds, not samples
def sliceBySeconds(X,begin, length):
    return X[int(begin*SR):int((begin+length)*SR)]
      
# Discrete Sine Transform
      
def dst(X):
    N = len(X)
    S = [0]*N
    for f in range(N):
        sum = 0
        for i in range(N):
            sum +=  sin( 2 * pi * f * i / N ) * X[i]
        S[f] = sum*2/N
    return S

