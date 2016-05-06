import subprocess
from os import walk
import fingerprint as fputil

f = []
for (dirpath, dirnames, filenames) in walk("music/wav"):
    f.extend(filenames)
    break

print("Creating fp's of files in", dirpath)
for filename in filenames:
	print(dirpath + "/" + filename, " -> ", "database/" + filename[0:len(filename)-4] +".fp")
	subprocess.call(['touch', "database/" + filename[0:len(filename)-4] +".fp"])
	fp = fputil.getFingerPrint(dirpath + "/" + filename)
	f = open( "database/" + filename[0:len(filename)-4] +".fp")
	f.write(str(fp))
	f.close()