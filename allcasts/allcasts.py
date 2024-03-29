#! python3
'''allcasts - A friendly command line podcast downloader

allcasts allows you to batch download podcasts from a given RSS feed.
allcasts can download all episodes, a range of episodes, or a specific episode.
Get started by running allcasts with no arguments or with the --help argument.
'''
__version__ = '0.1.9'
import os
import urllib
from os import path
import sys
import tqdm
import argparse
import colorama as col
import pyinputplus as pyip
import xmltodict
from pprint import pprint
from itunes_API import ItunesAPI


col.init()  # initialise colorama (required for Windows)

class AllCasts:

	def download(url, filepath):
		'''
		download a file from a url and save it to the filepath. Filepath must incllude filename. 

		filepath -> /path/to/directory/episode.mp3
		url -> https://example.com/episode.mp3
		'''
		import functools
		import pathlib
		import shutil
		import requests
		import tqdm
		
		r = requests.get(url, stream=True, allow_redirects=True)
		if r.status_code != 200:
			r.raise_for_status()  # Will only raise for 4xx codes, so...
			raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
		file_size = int(r.headers.get('Content-Length', 0))

		path = pathlib.Path(filepath).expanduser().resolve()
		path.parent.mkdir(parents=True, exist_ok=True)

		desc = "(Unknown total file size)" if file_size == 0 else ""
		r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed
		with tqdm.tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
			with path.open("wb") as f:
				shutil.copyfileobj(r_raw, f)

		return path

	def podcast_dict(url):
		'''
		returns a dictionary of the podcast feed from the given url
		'''
		with urllib.request.urlopen(url) as response:
			podcast_dict = xmltodict.parse(response.read())
		return podcast_dict

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
			for episode in all_podcast_episodes[start_number-1:end_number]:
				episode_title = episode['title']
				file_name = f"{episode_title}.mp3"
				episode_number = int(episode['itunes:episode'])
				if episode_number >= start_number and episode_number <= end_number:
					AllCasts.download_episode(episode['enclosure']['@url'], directory, file_name)
					print(f"\n{col.Fore.GREEN}🎧 Downloaded {episode_title}{col.Fore.RESET}")
		# if no episode tags are present, download episodes based on their order in the feed
		else:
			for episode in all_podcast_episodes[start_number-1:end_number]:
				episode_title = episode['title']
				file_name = f"{episode_title}.mp3"
				file_name = episode['enclosure']['@url'].split('/')[-1]
				# remove all text after '?' in the filename
				file_name = file_name.split('?')[0]
				AllCasts.download_episode(episode['enclosure']['@url'], directory, file_name)
				print(f"\n{col.Fore.GREEN}🎧 Downloaded {episode_title}{col.Fore.RESET}")
			print(f"\n{col.Fore.BLUE}--> 🎉 All podcast episodes downloaded!{col.Fore.RESET}")

	def download_episode(episode_url, filepath: str, filename="UNKNOWN"): 
		'''
		download the podcast episode from the individual episode's url (NOT the RSS feed url) and save it to the directory

		filepath -> /path/to/directory/episode.mp3
		'''	
		print(f"Downloading {episode_url}...")
		AllCasts.download(episode_url, str(filepath+"/"+filename))
		print(f"\n{col.Fore.GREEN}🎧 Downloaded {filename} to {filepath}{col.Fore.RESET}")

	def download_all_episodes(feed_url: str, directory: str, transcribe=False):
		'''
		download all podcasts from the rss feed url and save them to the directory
		'''
		# create the directory if it doesn't exist
		podcast_dict = AllCasts.podcast_dict(feed_url)
		for item in podcast_dict['rss']['channel']['item']:
			podcast_title = item['title']
			file_name = f"{podcast_title}.mp3"
			AllCasts.download_episode(item['enclosure']['@url'], directory, file_name)
			print(f"\n{col.Fore.GREEN}🎧 Downloaded {podcast_title}{col.Fore.RESET} as {col.Fore.BLUE}{file_name}{col.Fore.RESET}")
			if transcribe:
				AllCasts.transcribe_episode(path.join(directory, file_name))
		print(f"\n{col.Fore.BLUE}--> 🎉 All podcasts downloaded!{col.Fore.RESET}")

	def create_directory(directory):
		'''
		create the directory if it doesn't exist
		'''
		if not path.exists(directory):
			print(f"Creating directory {directory}")
			os.makedirs(directory)

	def download_all_podcasts_from_file(file_path, directory):
		'''
		download all podcasts from a text file and save them to the directory
		'''
		with open(file_path, 'r') as file:
			for line in file:
				AllCasts.download_all_episodes(line, directory)

	def itunes_search_cli():
		'''
		promt the user to search for a podcast, choose from the results and return the URL
		'''
		search_term = pyip.inputStr(prompt='Search for a podcast: ')
		# strip whitespace from search term, concatenate each word with '+'
		search_term = '+'.join(search_term.split())
		# search for the podcast
		results = ItunesAPI.podcast_search(search_term)
		if results:
			print(f"\n{col.Fore.BLUE}--> Search results: {col.Fore.RESET}")
			for i, result in enumerate(results):
				print(f"{col.Fore.GREEN}{i+1}{col.Fore.RESET}. {result['trackName']}")
			print(f"{col.Fore.BLUE}--> Choose a podcast from the list above: {col.Fore.RESET}")
			podcast_number = pyip.inputInt(prompt='', min=1, max=len(results))
			return results[podcast_number-1]['feedUrl']
		else:
			print(f"\n{col.Fore.RED}Error: No podcasts found!{col.Fore.RESET}")
			sys.exit(1)

	def transcribe_episode(mp3_file_path):
		'''
		Transcripe an MP3 file to text and write it to a file in the same directory as the MP3 file
		ATP303.mp3 -> ATP303.txt
		'''
		#TODO: implement whisper

def main():
	'''
	The main function will check for arguments, validate them, and call the appropriate function 
	OR if no arguments are passed, it will prompt the user for the required parameters
	'''
	# if arguments are passed, parse them:
	if len(sys.argv) > 1:
		# create the parser
		parser = argparse.ArgumentParser(description="A friendly command line podcast downloader - supports downloading entire feeds, individual episodes, and a range of episodes")
		mutually_exclusive = parser.add_mutually_exclusive_group(required=True)
		# define the arguments
		mutually_exclusive.add_argument("-f", "--feed", help="the url of the podcast feed", type=str, metavar="<URL>")
		mutually_exclusive.add_argument("-i", "--input", help="the input file containing a list of podcast feeds", type=str, metavar="<FILE>")
		parser.add_argument("-d", "--directory", help="the directory to save the podcast episodes", required=False, type=str, metavar="<DIRECTORY>")
		parser.add_argument("-t", "--transcribe", help="transcribe the podcast episodes to text", action="store_true")
		parser.add_argument("-s", "--start", help="the number of the first episode to download", type=int, metavar="<NUMBER>")
		parser.add_argument("-e", "--end", help="the number of the last episode to download", type=int, metavar="<NUMBER>")
		parser.add_argument("-a", "--all", help="download all episodes", action="store_true", required=False)
		parser.add_argument("-n", "--number", help="download a specific episode", type=int, metavar="<NUMBER>")
		parser.add_argument("-l", "--latest", help="download the latest episode", action="store_true", required=False)
		parser.add_argument("-v", "--version", help="display the version number", action="store_true", required=False)
		args = parser.parse_args()
		if args.directory:
			if not path.isdir(args.directory):
			# check if the directory argument is valid
				print(f"{col.Fore.RED}ERROR: The directory {args.directory} does not exist.{col.Fore.RESET}")
				sys.exit()
			else:
				directory = args.directory
		# if no directory is specified, use the current working directory
		else:
			directory = os.getcwd()
		if args.all:
			AllCasts.download_all_episodes(args.feed, directory, transcribe=args.transcribe)
		elif args.start and args.end:
			AllCasts.download_episode_range(args.feed, directory, args.start, args.end, transcribe=args.transcribe)
		elif args.number:
			AllCasts.download_episode_range(args.feed, directory, args.number, args.number, transcribe=args.transcribe)
		elif args.version:
			print(f"{col.Fore.BLUE}AllCasts v {col.Fore.RESET}")
		elif args.input:
			AllCasts.download_all_podcasts_from_file(args.input, directory)
		else:
			print(f"{col.Fore.RED}ERROR: You must specify either --all, --start, or --end{col.Fore.RESET}")
			sys.exit()
	else:
	# if no arguments are passed, prompt the user for the required information
		# display welcome message
		print(f"{col.Fore.RED}=========================================================={col.Fore.RESET}")
		print(f"{col.Fore.BLUE} ========= Welcome to the AllCasts App! ========{col.Fore.RESET}")
		print(f"{col.Fore.RED}=========================================================={col.Fore.RESET}")
		# ask if they want to search for a podcast
		mode = pyip.inputMenu(choices=['Search for a podcast','Enter URL', 'Quit'], prompt='Which would you like to do?\n', numbered=True)
		if mode == 'Search for a podcast':
			# if they want to search for a podcast, prompt the user
			feed_url = AllCasts.itunes_search_cli()
			download_mode = pyip.inputMenu(choices=['Download all episodes', 'Download a specific episode', 'Download an episode range', 'Quit'], prompt='Which would you like to do?\n', numbered=True)
			if download_mode == 'Download all episodes':
				AllCasts.download_all_episodes(feed_url, os.getcwd())
			elif download_mode == 'Download a specific episode':
				episode_number = pyip.inputInt(prompt='Enter the episode number: ')
				AllCasts.download_episode_range(feed_url, os.getcwd(), episode_number, episode_number)
			elif download_mode == 'Download an episode range':
				start_episode = pyip.inputInt(prompt='Enter the first episode number: ')
				end_episode = pyip.inputInt(prompt='Enter the last episode number: ')
				AllCasts.download_episode_range(feed_url, os.getcwd(), start_episode, end_episode)
		elif mode == 'Enter URL':
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
				AllCasts.download_all_episodes(pod_url, download_dir)
			except KeyboardInterrupt:
				sys.exit()
		sys.exit()

if __name__ == '__main__':
	main()
