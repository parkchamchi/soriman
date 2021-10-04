"""Mirror a directory to another directory"""

from util import util

import os
from os.path import join as joinpath
import shutil
import filecmp

from pprint import pprint as pprint

class Mirror():
	def __init__(self, src, dst):
		"""
		Select files to manipulate

		:param src: the source dir
		:param dst: the destination dir

		sets 
			src, dst,
			to_delete = ([dirs, files]), to_paste = ([dirs, files]), to_overwrite = [files]
		"""

		#check if the paths actually exist...
		if not os.path.exists(src):
			raise PathNotFound(src)
		if not os.path.exists(dst):
			raise PathNotFound(dst)
		
		self.src = src
		self.dst = dst

		#get the list of the both paths
		srclists = util.walkDir(src)
		dstlists = util.walkDir(dst)

		srcsets = (set(srclists[0]), set(srclists[1]))
		dstsets = (set(dstlists[0]), set(dstlists[1]))

		#First, select what to delete: dst - src
		self.to_delete = (list(dstsets[0] - srcsets[0]), list(dstsets[1] - srcsets[1]))
		
		#Second, select what to copy & paste: src - dst
		self.to_paste = (list(srcsets[0] - dstsets[0]), list(srcsets[1] - dstsets[1]))

		#Lastly, select what to change: src & dst files and compare
		self.to_overwrite = []

		to_compare = srcsets[1] & dstsets[1]
		for filename in to_compare:
			if not filecmp.cmp(joinpath(src, filename), joinpath(dst,filename)):
				self.to_overwrite.append(filename)

	def show(self):
		"Returns False if the directories are the same and True otherwise."

		#Check the differences
		if not (self.to_delete[0] or self.to_delete[1] or self.to_paste[0] or self.to_paste[1] or self.to_overwrite):
			print("The directories are the same.")
			return False

		#Show...
		print("To be deleted:")
		print("Directories:")
		pprint(util.returnNoneStrForFalse(self.to_delete[0]))
		print("Files:")
		pprint(util.returnNoneStrForFalse(self.to_delete[1]))
		print()

		print("To be pasted:")
		print("Directories:")
		pprint(util.returnNoneStrForFalse(self.to_paste[0]))
		print("Files:")
		pprint(util.returnNoneStrForFalse(self.to_paste[1]))
		print()

		print("To be overwritten")
		pprint(util.returnNoneStrForFalse(self.to_overwrite))
		print()

		return True

	def mirror(self):
		"""Execute"""

		archivedir = "./archive"
		archivefilename = archivedir + "/archive"
		archivetype = "zip"
		movecount = 0

		if not os.path.exists(archivedir):
			os.mkdir(archivedir)
		
		#Delete...
		#the files first
		for filename in self.to_delete[1]:
			#instead of os.remove, move it to the archive directory
			#first, rename it so filenames don't clash
			if os.path.exists(joinpath(archivedir, os.path.basename(filename))):
				newfilename = filename + str(movecount)
				os.rename(joinpath(self.dst, filename), joinpath(self.dst, newfilename))
				filename = newfilename
				movecount += 1
			shutil.move(joinpath(self.dst, filename), archivedir)

		#then the directories
		#sort the list reverse-alphabetic order
		#so that the subdirectory can be deleted first
		self.to_delete[0].sort(reverse = True)
		for dirname in self.to_delete[0]:
			os.rmdir(joinpath(self.dst, dirname))

		#Paste...
		#the directories first
		#sort the list so that the parent folder can be made first
		self.to_paste[0].sort()
		for dirname in self.to_paste[0]:
			os.makedirs(joinpath(self.dst, dirname))
		
		#then the files
		for filename in self.to_paste[1]:
			shutil.copy(joinpath(self.src, filename), joinpath(self.dst, filename))

		#Overwrite...
		for filename in self.to_overwrite:
			if os.path.exists(joinpath(archivedir, os.path.basename(filename))):
				newfilename = filename + str(movecount)
				os.rename(joinpath(self.dst, filename), joinpath(self.dst, newfilename))
				movecount += 1
			else:
				newfilename = filename
			shutil.move(joinpath(self.dst, newfilename), archivedir)
			shutil.copy(joinpath(self.src, filename), joinpath(self.dst, filename))

		#Archive the archivedir
		shutil.make_archive(archivefilename, archivetype, archivedir)
		for file in os.listdir(archivedir):
			if file == os.path.basename(archivefilename + "." + archivetype):
				continue
			os.remove(joinpath(archivedir, file))

		print("Done.")

class PathNotFound(Exception):
	pass