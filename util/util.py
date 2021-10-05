import os
from os.path import join as joinpath
import shutil

def walkDir(path):
	"""
	Returns all directorys and files with dir_path + (filename/dirname)
	Root path will not be printed

	:param path: path
	:param print_root: whether the root path would be included
	"""
	
	#1d lists of path + filename
	dir_list = []
	file_list = []
	
	#to delete the root path
	pthlen = len(path) + 1

	for dirpath, dirnames, filenames in os.walk(path):
		dirpath = dirpath[pthlen:]

		for dirname in dirnames:
			dir_list.append(joinpath(dirpath, dirname))
		for filename in filenames:
			file_list.append(joinpath(dirpath, filename))

	return (dir_list, file_list)

def returnNoneStrForFalse(value):
	if (value):
		return value
	else:
		return "None"

def getAllowedPath(path):
	not_alloweds = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|", "."]
	for not_allowed in not_alloweds:
		path = path.replace(not_allowed, "_")
	return path