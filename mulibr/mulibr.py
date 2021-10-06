"""The music library"""

from util import util
from util.util import getAllowedPath as topath

from tinytag import TinyTag

import os
from os.path import join as joinpath
from pprint import pprint as pprint
import shutil

class Mulibr():
	def __init__(self):
		self.artists = []

	def __str__(self):
		return str(self.artists)

	def __repr__(self):
		return self.__str__()

	def addArtist(self, artistname):
		new_artist = Artist(artistname)
		self.artists.append(new_artist)
		return new_artist

	def hasArtist(self, artistname):
		for artist in self.artists:
			if artistname == artist.name:
				return artist

		return False

	def getArtist(self, artistname):
		artist = self.hasArtist(artistname)
		if not artist:
			artist = self.addArtist(artistname)

		return artist

	@property
	def artistnames(self):
		return [artist.name for artist in self.artists]

	@property
	def albumcount(self):
		count = 0
		for artist in self.artists:
			count += len(artist.albums)
		return count

	def read(self, src):
		"""
		Read music files in src
		Returns: list of non-music files
		"""

		formats = [".mp3", ".flac", ".m4a"]

		#Get all files from src
		files = util.walkDir(src)[1]
		
		#Select music formats
		musicfiles = []
		otherfiles = []

		for file in files:
			#Get the extension
			ext = os.path.splitext(file)[1]
			if ext.lower() in formats:
				musicfiles.append(file)
			else:
				otherfiles.append(file)
		
		#Read music files
		tracks = []
		for musicfile in musicfiles:
			filetags = TinyTag.get(joinpath(src, musicfile))

			track = {}
			track["artist"] = filetags.artist.strip()
			track["album"] = filetags.album.strip()
			track["path"] = musicfile

			tracks.append(track)

		#Organize it
		for track in tracks:
			artist = self.getArtist(track["artist"])
			album = artist.getAlbum(track["album"])
			album.addTrack(track["path"])

		return otherfiles

class Mainlibr(Mulibr):
	def __init__(self, path):
		super().__init__()

		self.path = path

		if os.path.exists(self.path):
			#Read files in path
			super().read(self.path)

			#Also read empty artists: mostly created by exception
			for dir_artistname in next(os.walk(path))[1]:
				if not dir_artistname in self.artistnames:
					#Found the empty artist
					self.addArtist(dir_artistname)

			#Also read empty albums
			for artistdir in next(os.walk(path))[1]:
				for albumdir in next(os.walk(joinpath(path, artistdir)))[1]:
					if not os.listdir(joinpath(path, artistdir, albumdir)):
						#Found the empty album
						self.getArtist(artistdir).addAlbum(albumdir)

		else:
			os.mkdir(self.path)

	def readDir(self, src):
		srclibr = Mulibr()
		otherfiles = srclibr.read(src)

		ignored = []

		for src_artist in srclibr.artists:
			main_artist = self.hasArtist(src_artist.name)
			if not main_artist:
				#Create the aritist directory
				try:
					os.mkdir(self.getArtistPath(src_artist))
				except FileExistsError:
					#The lowercase/uppercase clash
					pass

				main_artist = self.addArtist(src_artist.name)

			for src_album in src_artist.albums:
				main_album =  main_artist.hasAlbum(src_album.title)
				if main_album:
					#album clash
					print("The album \"%s\" - \"%s\" is already in main library..." % (src_artist.name, src_album.title))
					print("In source library (to be moved):")
					pprint(src_album.tracks)
					print("In main library (to be overwritten):")
					pprint(main_album.tracks)
					print()

					#Get confirm
					confirm = input("Delete the directory and overwrite? (y/n): ")
					if (confirm.lower() != "y"):
						print("Ignored...")
						ignored.append(src_album.tracks)
						continue #ignore
					else:
						#Delete the main album
						shutil.rmtree(self.getAlbumPath(main_artist, main_album))
						del main_album
				
				#Create new album dir and obj...
				os.mkdir(self.getAlbumPath(src_artist, src_album))
				main_album = main_artist.addAlbum(src_album.title)

				#Move...
				for track in src_album.tracks:
					shutil.move(joinpath(src, track), self.getAlbumPath(main_artist, main_album))
				print("Moved %s - %s..." % (main_artist.name, main_album.title))

		#Clear the src folder
		print("\n\n||||||||||||||||||||||||||||||||||||||")
		print("These files will be deleted:")

		#Gather extentions of otherfiles
		exts = {}
		for file in otherfiles:
			ext = os.path.splitext(file)[1]
			if ext in exts:
				exts[ext] += 1
			else:
				exts[ext] = 0
		pprint(otherfiles)
		print(exts)

		pprint(ignored)

		confirm = input("Clear the src directory? (y/n): ")
		if confirm.lower() == "y":
			shutil.rmtree(src)
			os.mkdir(src)
			print("Deleted %s." % src)

		print("Now there are %d albums in main library." % self.albumcount)

	def getArtistPath(self, artist):
		return joinpath(self.path, topath(artist.name))

	def getAlbumPath(self, artist, album):
		return joinpath(self.path, topath(artist.name), topath(album.title))

class Artist():
	def __init__(self, name):
		self.name = name

		self.albums = []

	def __str__(self):
		return self.name + ":\n" + str(self.albums) + "\n"

	def __repr__(self):
		return self.__str__()

	def addAlbum(self, albumtitle):
		new_album = Album(albumtitle)
		self.albums.append(new_album)
		return new_album
	
	def hasAlbum(self, albumtitle):
		for album in self.albums:
			if albumtitle == album.title:
				return album

		return False

	def getAlbum(self, albumtitle):
		album = self.hasAlbum(albumtitle)
		if not album:
			album = self.addAlbum(albumtitle)

		return album

class Album():
	def __init__(self, title):
		self.title = title

		self.tracks = []

	def __str__(self):
		return self.title + ": " + str(self.tracks) + "\n"

	def __repr__(self):
		return self.__str__()

	def addTrack(self, track):
		self.tracks.append(track)