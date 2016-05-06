import subprocess
from os import walk
import fingerprint as fputil
import pickle

f = []
for (dirpath, dirnames, filenames) in walk("music/wav"):
    f.extend(filenames)
    break

print("Creating fp's of files in", dirpath)
for filename in filenames:
	print(dirpath + "/" + filename, " -> ", "database/" + filename[0:len(filename)-4] +".fp")
	subprocess.call(['touch', "database/" + filename[0:len(filename)-4] +".fp"])
	subprocess.call(['chmod', "777" ,"database/" + filename[0:len(filename)-4] +".fp"])
	fp = fputil.getFingerPrint(dirpath + "/" + filename)
	pickle.dump(fp, "database/" + filename[0:len(filename)-4] +".fp")