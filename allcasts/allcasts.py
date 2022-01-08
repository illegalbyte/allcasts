#! python3
import pyinputplus as pyip
import colorama as col
import wget
import urllib
import xmltodict
from os import path
import os

# initialise colorama (required for Windows)
col.init()

class AllCasts:

	def podcast_dict(url):
		'''
		returns a dictionary of the podcast feed
		'''
		with urllib.request.urlopen(url) as response:
			podcast_dict = xmltodict.parse(response.read())
		return podcast_dict

	def download_episode(feed_url, directory, episode_number):
		'''
		download a specific podcast episode from the rss feed url and save it to the directory
		'''
		podcast_dict = AllCasts.podcast_dict(feed_url)
		episode_title = podcast_dict['rss']['channel']['item'][episode_number]['title']
		file_name = f"{episode_title}.mp3"
		AllCasts.download_podcast(podcast_dict['rss']['channel']['item'][episode_number]['enclosure']['@url'], directory, file_name)
		print(f"\n{col.Fore.GREEN}🎧 Downloaded {episode_title}{col.Fore.RESET}")
		print(f"\n{col.Fore.BLUE}--> 🎉 Podcast downloaded!{col.Fore.RESET}")

	def download_episode_range(feed_url, directory, start_number, end_number):
		'''
		download a range of podcast episodes from a given rss feed url and save them to the directory
		'''
		podcast_dict = AllCasts.podcast_dict(feed_url)
		for item in podcast_dict['rss']['channel']['item'][start_number:end_number]:
			podcast_title = item['title']
			file_name = f"{podcast_title}.mp3"
			AllCasts.download_podcast(item['enclosure']['@url'], directory, file_name)
			print(f"\n{col.Fore.GREEN}🎧 Downloaded {podcast_title}{col.Fore.RESET}")
		print(f"\n{col.Fore.BLUE}--> 🎉 All podcasts downloaded!{col.Fore.RESET}")

	def download_podcast(episode_url, directory, filename):
		'''
		download the podcast episode from the individual episode's url (NOT the RSS feed url) and save it to the directory
		'''	
		print(f"Downloading {episode_url}...")
		wget.download(episode_url, out=directory, bar=wget.bar_thermometer)
		# TODO: rename files to the title of the podcast episode with datestamp


	def download_all_podcasts(feed_url, directory):
		'''
		download all podcasts from the rss feed url and save them to the directory
		'''
		# create the directory if it doesn't exist
		podcast_dict = AllCasts.podcast_dict(feed_url)
		for item in podcast_dict['rss']['channel']['item']:
			podcast_title = item['title']
			file_name = f"{podcast_title}.mp3"
			AllCasts.download_podcast(item['enclosure']['@url'], directory, file_name)
			print(f"\n{col.Fore.GREEN}🎧 Downloaded {podcast_title}{col.Fore.RESET}")
		print(f"\n{col.Fore.BLUE}--> 🎉 All podcasts downloaded!{col.Fore.RESET}")


	def create_directory(directory):
		'''
		create the directory if it doesn't exist
		'''
		if not path.exists(directory):
			print(f"Creating directory {directory}")
			os.makedirs(directory)
			

def main():
	# welcome message
	print(f"{col.Fore.RED}=========================================================={col.Fore.RESET}")
	print(f"{col.Fore.BLUE} ========= Welcome to the AllCasts App! ========{col.Fore.RESET}")
	print(f"{col.Fore.RED}=========================================================={col.Fore.RESET}")
	# prompt the user for the url
	pod_url = pyip.inputURL(prompt=f'Please enter the URL of the podcast feed you want to download: ')
	# prompt the user for the directory
	download_dir = pyip.inputFilepath(prompt='Please enter the directory you want to download the podcast to [leave blank for current dir]: ', blank=True)
	# if the user didn't enter a directory, use the current directory
	if download_dir == '' or download_dir == '.':
		download_dir = path.abspath('.')
	# inform the user the downloads will begin
	print(f"Downloading all podcasts from {pod_url} to {download_dir}")
	# download the podcast
	AllCasts.download_all_podcasts(pod_url, download_dir)
	

if __name__ == '__main__':
	main()
