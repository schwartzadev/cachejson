# cache_json.py
import requests
import json
import os

folder_name = 'json-cache-py'

class CacheJson(object):
	"""Interface with a JSON object through the cache.
	Download a given JSON resource from a given URL
	and retrieve the data from a cache if possible.
	
	Note that __init__ takes 1 or 2 values. The second
	is an optional boolean, 'update,' which defines whether
	a user wants to update the file or retrieve the
	older version. (True means use the file should be
	overwritten, false means it should be read.)
	"""
	def __init__(self, url, update=False):
		self.url = url
		self.make_filename()
		self.update = update

		self.make_cache_directory()

	def download(self):
		"""retrieve JSON data via requests.get"""
		return requests.get(self.url).json()

	def save(self):
		"""save JSON data to a file"""
		with open('{}/{}'.format(self.directory, self.filename), 'w') as out:
			json.dump(self.raw, out)

	def make_cache_directory(self):
		"""makes the directory for saving cached files"""
		try:
			full = os.path.join(os.path.expanduser("~"), folder_name)
			self.directory = full
			os.makedirs(full) # will throw errors
		except FileExistsError as e:
			pass

	def make_filename(self):
		"""generate the filename for the saved json file"""
		self.filename = '{}.json'.format(self.url.translate({
			ord('/'): '=',
			ord(':'): '-'
			}))
		return self.filename

	def file_exists(self):
		"""see if this JSON file is already cached"""
		return os.path.isfile('{}/{}'.format(self.directory, self.filename))

	def load(self):
		"""loads JSON from the cached file to an object"""
		with open('{}/{}'.format(self.directory, self.filename)) as file:
			return json.load(file)

	def json(self):
		"""Returns the JSON data associated with the URL.
		(Done either by reading from the cache or retrieving from online.)
		"""
		if self.file_exists() and not self.update:
			return self.load()

		self.raw = self.download()
		self.save()
		return self.raw

URL = 'https://api.github.com/users/schwartzadev'
obj = CacheJson(URL).json()
print(obj)
