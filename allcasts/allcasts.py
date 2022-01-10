#! python3
'''allcasts – A friendly command line podcast downloader

allcasts allows you to batch download podcasts from a given RSS feed.
allcasts can download all episodes, a range of episodes, or a specific episode.
Get started by running allcasts with no arguments or with the --help argument.
'''
__version__ = '0.1.6'
import os
import urllib
from os import path
import sys

import argparse
import colorama as col
import pyinputplus as pyip
import wget
import xmltodict
from pprint import pprint

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
		print(f"Downloading episodes {col.Fore.GREEN}{start_number}{col.Fore.RESET} to {col.Fore.GREEN}{end_number}{col.Fore.RESET}...")
		podcast_dict = AllCasts.podcast_dict(feed_url)
		# swap values of start and end numbers if the start number is greater than the end number
		if start_number > end_number:
			start_number, end_number = end_number, start_number
		# create a list of the podcast episodes
		all_podcast_episodes = podcast_dict['rss']['channel']['item']
		# reverse list of episodes so that the oldest episodes are downloaded first
		all_podcast_episodes.reverse()
		# if the podcast has episode tags, use those to download the episode range
		if 'itunes:episode' in podcast_dict['rss']['channel']['item'][0]:
			for episode in all_podcast_episodes[:]:
				podcast_title = episode['title']
				file_name = f"{podcast_title}.mp3"
				episode_number = int(episode['itunes:episode'])
				if episode_number >= start_number and episode_number <= end_number:
					AllCasts.download_podcast(episode['enclosure']['@url'], directory, file_name)
					print(f"\n{col.Fore.GREEN}🎧 Downloaded {podcast_title}{col.Fore.RESET}")
		# if no episode tags are present, download episodes based on their order in the feed
		else:
			for episode in all_podcast_episodes[start_number-1:end_number]:
				podcast_title = episode['title']
				file_name = f"{podcast_title}.mp3"
				AllCasts.download_podcast(episode['enclosure']['@url'], directory, file_name)
				print(f"\n{col.Fore.GREEN}🎧 Downloaded {podcast_title}{col.Fore.RESET}")
			print(f"\n{col.Fore.BLUE}--> 🎉 All podcast episodes downloaded!{col.Fore.RESET}")

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
	'''
	The main function will check for arguments, validate them, and call the appropriate function 
	OR if no arguments are passed, it will prompt the user for the required information
	'''

	# if arguments are passed, parse them:
	if len(sys.argv) > 1:
		# create the parser
		parser = argparse.ArgumentParser(description="A friendly command line podcast downloader - supports downloading entire feeds, individual episodes, and a range of episodes")
		# define the arguments
		parser.add_argument("-d", "--directory", help="the directory to save the podcast episodes", required=False, type=str, metavar="<DIRECTORY>")
		parser.add_argument("-f", "--feed", help="the url of the podcast feed", required=True, type=str, metavar="<URL>")
		parser.add_argument("-s", "--start", help="the number of the first episode to download", type=int, metavar="<NUMBER>")
		parser.add_argument("-e", "--end", help="the number of the last episode to download", type=int, metavar="<NUMBER>")
		parser.add_argument("-a", "--all", help="download all episodes", action="store_true", required=False)
		parser.add_argument("-n", "--number", help="download a specific episode", type=int, metavar="<NUMBER>")
		parser.add_argument("-l", "--latest", help="download the latest episode", action="store_true", required=False)
		parser.add_argument("-v", "--version", help="display the version number", action="store_true", required=False)
		args = parser.parse_args()

		# check if the directory argument is valid
		if args.directory:
			if not path.isdir(args.directory):
				print(f"{col.Fore.RED}ERROR: The directory {args.directory} does not exist.{col.Fore.RESET}")
				sys.exit()
			else:
				directory = args.directory
		else:
		# if no directory is specified, use the current working directory
			directory = os.getcwd()

		if args.all:
			AllCasts.download_all_podcasts(args.feed, directory)
		elif args.start and args.end:
			AllCasts.download_episode_range(args.feed, directory, args.start, args.end)
		elif args.number:
			AllCasts.download_episode_range(args.feed, directory, args.number, args.number)
		elif args.version:
			print(f"{col.Fore.BLUE}AllCasts v {col.Fore.RESET}")
		else:
			print(f"{col.Fore.RED}ERROR: You must specify either --all, --start, or --end{col.Fore.RESET}")
			sys.exit()


	# if no arguments are passed, prompt the user for the required information
	else:
		# display welcome message
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
		try:
			AllCasts.download_all_podcasts(pod_url, download_dir)
		except KeyboardInterrupt:
			sys.exit()
		sys.exit()

if __name__ == '__main__':
	main()
