# Sean Smith
# CS591 Audio 
# Spring 2016
# this file simply returns the fingerprint of a song or sample of a song

import audioUtilities as au
import numpy as np
import matplotlib.pyplot as plt

WINDOW_SIZE    = 4096
SLIDE_INTERVAL = 2048
THRESHHOLD = .8
SR = 44100
MAX_AMP = 2**15 - 1


def realFFT(X):
	WR = SR/len(X)
	return [(i*WR, 2.0 * np.absolute(x)/len(X)) for i, x in enumerate(np.fft.rfft(X))]

def pickPeaks(P):
	s = []
	m = max(P, key=lambda x: x[1])[1] * THRESHHOLD 
	for f,p in P:
		if p > m:
			s.append(f)
	return s

def graphFingerPrint(fp, fp2=None):
	X = []
	Y = []
	for i,f in enumerate(fp):
		for k in f:
			X.append((i*WINDOW_SIZE) / (SR*2))
			Y.append(k)
	
	plt.xlabel("Time")
	plt.ylabel("Frequency")
	plt.axis([0.0,max(X), 0,max(Y)])

	plt.scatter(X,Y)
	plt.show()


def getFingerPrint(path):
	print("Creating fingerprint of ",path)
	X = au.readWaveFile(path)
	l = len(X)
	i = 0
	fp = []
	while i <= (l - 4096): 
		P = realFFT(X[i:(i+WINDOW_SIZE)])
		p = pickPeaks(P)
		print(p)
		fp.append(sorted(p))
		# au.graphSpectrum(X[i:(i+WINDOW_SIZE)])
		i += SLIDE_INTERVAL

	print("Generated", len(fp), "windows.")
	return fp

# Gets the difference between two lists of lists
# the number of lists is garaunteed to be the same
def diff(l1, l2):
	sum = 0
	for i in range(len(l1)):
		r = min(len(l1[i]), len(l2[i]))
		for j in range(r):
			sum += abs(l1[i][j] - l2[i][j])
	return sum

# compares fingerprint 2 to fingerprint 1, sliding it over the entire thing
# returns a list of numbers
def match(fp1, fp2):
	lfp1 = len(fp1)
	lfp2 = len(fp2)

	diff_list = []
	i = 0
	while i <= (lfp1 - lfp2):
		diff_list.append(diff(fp1[i:(i+len(fp2))], fp2))
		i += 1

	return diff_list

fp1 = getFingerPrint("music/BluesGuitar.wav")


fp2 = getFingerPrint("music/BluesGuitar1_2.wav")
graphFingerPrint(fp1)

Y = match(fp1, fp2)
X = [(x*WINDOW_SIZE) / (SR*2) for x in range(len(Y))]
plt.plot(X,Y)
plt.show()

val, idx = min((val, idx) for (idx, val) in enumerate(Y))

print((idx*WINDOW_SIZE) / (SR*2), val)

# print("matching the files.")


# print("graphing.")



# print (X)

# simple test of FFT
# X = au.readWaveFile("music/BluesGuitar.wav")
# au.writeWaveFile("music/BluesGuitar1_2.wav", X[(SR * 1):(SR *2)])
# S = au.graphSpectrum(X[0:44100])
# S = realFFT(X[0:44100])


# print (au.SR, len(X)/au.SR)
# print (F)



