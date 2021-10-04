"""The music library"""

from util import util

from tinytag import TinyTag

import os
from os.path import join as joinpath

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

	def read(self, src):
		"""Read music files in src"""

		formats = [".mp3", ".flac", "m4a"]

		#Get all files from src
		files = util.walkDir(src)[1]
		
		#Select music formats
		musicfiles = []
		otherfiles = []

		for file in files:
			#Get the extension
			ext = os.path.splitext(file)[1]
			if ext in formats:
				musicfiles.append(file)
			else:
				otherfiles.append(file)
		
		#Read music files
		tracks = []
		for musicfile in musicfiles:
			filetags = TinyTag.get(joinpath(src, musicfile))

			track = {}
			track["artist"] = filetags.artist
			track["album"] = filetags.album
			track["path"] = musicfile

			tracks.append(track)

		#Organize it
		for track in tracks:
			artist = self.getArtist(track["artist"])
			album = artist.getAlbum(track["album"])
			album.addTrack(track["path"])

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