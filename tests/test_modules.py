import unittest
import os


class TestWget(unittest.TestCase):
	def test_wget_installed(self):
		'''
		wget should be available
		'''
		try:
			import wget
		except ImportError:
			self.fail("wget not available - run 'pip install wget'")

	def test_wget_download(self):
		'''
		wget should be able to download a file
		'''
		import wget
		wget.download("https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png", "google.png")
		self.assertTrue(os.path.isfile("google.png"))
		os.remove("google.png")

class TestXMLtoDict(unittest.TestCase):
	def test_xmltodict_installed(self):
		'''
		xmltodict should be available
		'''
		try:
			import xmltodict
		except ImportError:
			self.fail("xmltodict not available - run: 'pip install xmltodict'")

	def test_xmltodict_parse(self):
		'''
		xmltodict should be able to parse a file
		'''
		import xmltodict
		with open('example_rss.xml', 'r') as f:
			podcast_dict = xmltodict.parse(f.read())
		self.assertTrue(podcast_dict)

	def test_xmltodict_parse_url(self):
		'''
		xmltodict should be able to parse a url
		'''
		import urllib
		import xmltodict
		with urllib.request.urlopen('https://www.npr.org/rss/podcast.php?id=510289') as url:
			podcast_dict = xmltodict.parse(url.read())
		self.assertTrue(podcast_dict)

class TestColorama(unittest.TestCase):
	def test_colorama_installed(self):
		'''
		colorama should be available
		'''
		try:
			import colorama
		except ImportError:
			self.fail("colorama not available - run: 'pip install colorama'")
	
	def test_colorama_init(self):
		'''
		colorama should be able to init
		'''
		import colorama
		colorama.init()
	
	def test_colorama_foreground(self):
		'''
		colorama should be able to set foreground color
		'''
		import colorama as col
		col.init()
		col.Fore.GREEN
		col.Fore.RESET
	
	def test_colorama_background(self):
		'''
		colorama should be able to set background color
		'''
		import colorama as col
		col.init()
		col.Back.GREEN
		col.Back.RESET