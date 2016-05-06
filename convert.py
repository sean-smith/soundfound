import subprocess
from os import walk

f = []
for (dirpath, dirnames, filenames) in walk("music/mp3"):
    f.extend(filenames)
    break

print("converting files in", dirpath)
for filename in filenames:
	print(dirpath + "/" + filename, " -> ", "music/wav/" + filename[0:len(filename)-4].replace(" ", "_") +".wav")
	subprocess.call(['ffmpeg', '-i', dirpath + "/" + filename, "music/wav/" + filename[0:len(filename)-4].replace(" ", "_") +".wav"])
