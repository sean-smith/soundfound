# Sean Smith
# CS591 Audio 
# Spring 2016
import fingerprint as fputil
import pickle
from os import walk

def readfpFile(path):
	fp = []
	with open(path, 'rb') as pickle_file:
			fp = pickle.load(pickle_file)
			pickle_file.close()
	return fp


def search_db(fp2):
	search_list = []
	f = []
	for (dirpath, dirnames, filenames) in walk("database/"):
		f.extend(filenames)
		break
	for filename in filenames:
		print("Searching ", filename)
		fp1 = readfpFile("database/"+filename)
		time, acc = fputil.match(fp1, fp2)
		print("Accuracy ", acc)
		search_list.append((filename, time, acc))

	print ("\n\nSong is:\n===============")
	match = min(search_list, key=lambda x: x[2])
	print (match[0][:-3], "	@	", match[1])


fp2 = readfpFile("database/Big_Sean_-_I_Don't_Fuck_With_You.fp") 

search_db(fp2[30:300])