from mulibr import mulibr
from mirror import mirror

import sys
import os
from pprint import pprint as pprint

def getMainPath():
	filename = "pref"

	#Try to fetch from the file
	if os.path.exists(filename):
		#read...
		with open(filename, "rt") as file:
			mainpath = file.read()
		if os.path.exists(mainpath):
			confirm = input("Is the main library at %s? (y/n): " % mainpath)
			if confirm:
				return mainpath

	while True:
		mainpath = input("Input the main library...: ")
		if os.path.exists(mainpath):
			#write...
			with open(filename, "wt") as file:
				file.write(mainpath)

			return mainpath
		else:
			print("Path not found...")

print("Sorinet: Music file organization program")

#Get the source directory path
src = ""
if len(sys.argv) > 1:
	confirm = input("Are you sure the source folder is %s? (y/n): " % sys.argv[1])
	if confirm.lower() == "y":
		src = sys.argv[1]

if not src:
	#Get src
	while True:
		src = input("Input the source directory...: ")
		if not os.path.exists(src):
			print("Couldn't locate the path...")
		else:
			break

#Get the main library path
mainpath = getMainPath()

#Read src
mainlibr = mulibr.Mainlibr(mainpath)
mainlibr.readDir(src)

#Mirror
confirm = input("Would you mirror the library to other directory? (y/n): ")
if confirm.lower() == "y":
	while True:
		dstpath = input("Input the mirror path...: ")
		if os.path.exists(dstpath):
			print("Warning: the contents of this directory will be gone!")
			pprint(os.listdir(dstpath))
			confirm = input("Proceed? (y/n): ")
			if confirm.lower() == "y":
				break
		else:
			print("Creating directory...")
			os.mkdir(dstpath)
			break
	
	#Show
	mirrorobj = mirror.Mirror(mainpath, dstpath)
	mirrorobj.show()
	confirm = input("Are you sure? (y/n): ")
	if confirm.lower() == "y":
		mirrorobj.mirror()