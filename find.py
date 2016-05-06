# Sean Smith
# CS591 Audio 
# Spring 2016
import fingerprint as fpu
import pickle
from os import walk
from createdb import getFilesInPath
from listen import record_to_file

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def readfpFile(path):
	fp = []
	with open(path, 'rb') as pickle_file:
			fp = pickle.load(pickle_file)
			pickle_file.close()
	return fp


def search_db(fp2):
	search_list = []

	filenames = getFilesInPath("database/")
	for filename in filenames:
		print("Searching ", filename)
		fp1 = readfpFile("database/"+filename)
		time, acc = fpu.match(fp1, fp2)
		print("Accuracy ", acc)
		search_list.append((filename, time, acc))

	print ("\n\nSong is:\n==============="+ bcolors.OKGREEN)
	match = min(search_list, key=lambda x: x[2])
	print (match[0][:-3], "	@	", str(match[1])+ bcolors.ENDC)


print(bcolors.OKGREEN + "Welcome to SoundFound ..." + bcolors.ENDC)
print(bcolors.OKBLUE+"Please play a song starting now\n===================="+bcolors.ENDC)
# record_to_file('tmp.wav')
print("Done - result written to tmp.wav")

# fp2 = fpu.getFingerPrint("tmp.wav")
# fp2 = fpu.getFingerPrint("music/wav/Cage_The_Elephant_-_Back_Against_the_Wall.wav", start=4, end=9)
# search_db(fp2)
# fp2 = fpu.getFingerPrint("music/wav/Alesso_-_Heroes_(we_could_be).wav", start=4, end=9)
# search_db(fp2)
fp2 = fpu.getFingerPrint("music/wav/Big_Wild_-_Aftergold.wav", start=4, end=9)
# search_db(fp2)
# fp2 = fpu.getFingerPrint("music/wav/Big_Sean_-_I_Don't_Fuck_With_You.wav", start=4, end=9)
# search_db(fp2)

# fp2 = readfpFile("database/Big_Sean_-_I_Don't_Fuck_With_You.fp") 

search_db(fp2)

print(fpu.samples_to_seconds(270))