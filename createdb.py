import subprocess
from os import walk
import fingerprint as fputil
import pickle


def writefpFile(path, fp):
	with open(path, 'wb') as pickle_file:
		pickle.dump(fp, pickle_file)
		pickle_file.close()


def getFilesInPath(path):
	f = []
	for (dirpath, dirnames, filenames) in walk(path):
		f.extend(filenames)
		break
	return filenames

dirpath = "music/wav"
filenames = getFilesInPath(dirpath)
print("Creating fp's of files in", dirpath)

for filename in filenames:
	path = "database/" + filename[0:len(filename)-4] +".fp"
	print(dirpath + "/" + filename, " -> ", path)
	subprocess.call(['touch', path])
	fp = fputil.getFingerPrint(dirpath + "/" + filename)
	writefpFile(path)