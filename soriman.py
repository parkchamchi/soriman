from mulibr import mulibr
from mirror import mirror

import sys
import os

print("Sorinet: Music file organization program")

src = ""
if len(sys.argv) > 1:
	confirm = input("Are you sure the source folder is %s? (y/n): ")
	if confirm.lower() == "y":
		src = sys.argv[1]

if not src:
	#Get src
	while True:
		path = input("Input the source directory...")
		if not os.path.exists(path):
			print("Couldn't locate the path...")
		else:
			break

#Get the main library path
pass