from allcasts import AllCasts
import unittest
import os

# test feeds:
# redscare podcast
# http://redscarepodcast.libsyn.com/rss

class TestAllCasts(unittest.TestCase):
	def test_allcasts_installed(self):
		'''
		allcasts should be available
		'''
		try:
			import allcasts
		except ImportError:
			self.fail("allcasts not available - run: 'pip install allcasts'")

	# def test_allcasts_download_all_podcasts(self):
	# 	'''
	# 	allcasts should be able to download all podcasts
	# 	'''
	# 	from allcasts import AllCasts
	# 	AllCasts.download_all_podcasts('https://www.npr.org/rss/podcast.php?id=510289', '.')
	# 	self.assertTrue(os.path.exists('NPR-AllCasts.mp3'))

	def test_allcasts_create_directory(self):
		'''
		allcasts should be able to create a directory
		'''
		from allcasts import AllCasts
		AllCasts.create_directory('test_directory')
		self.assertTrue(os.path.exists('test_directory'))
		os.rmdir('test_directory')

	def test_allcasts_download_podcast(self):
		'''
		allcasts should be able to download entire feed
		'''
		from allcasts import AllCasts
		AllCasts.download_episode("https://traffic.libsyn.com/atpfm/atp464.mp3",
		                          directory='.', filename='atp464.mp3')
		self.assertTrue(os.path.exists('atp464.mp3'))
		os.remove('atp464.mp3')
