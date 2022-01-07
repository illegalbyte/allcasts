#! python3

import pyinputplus as pyip
import colorama as col
import wget
import urllib
import xmltodict
from os import path
import os

# initialise colorama for Windows
col.init()

def download_podcast(url, directory, filename):
    print(f"Downloading {url}")
    wget.download(url, out=directory, bar=wget.bar_thermometer)


def download_all_podcasts(url, directory):
    create_directory(directory)
    XML = urllib.request.urlopen(url).read()
    podcast_dict = xmltodict.parse(XML)
    for item in podcast_dict['rss']['channel']['item']:
        podcast_title = item['title']
        file_name = f"{podcast_title}.mp3"
        download_podcast(item['enclosure']['@url'], directory, file_name)
        print(f"\n{col.Fore.GREEN}🎧 Downloaded {podcast_title}{col.Fore.RESET}")
    print(f"\n{col.Fore.BLUE}--> 🎉 All podcasts downloaded!{col.Fore.RESET}")


def create_directory(directory):
    if not path.exists(directory):
        print(f"Creating directory {directory}")
        os.makedirs(directory)

# test url:
# https://redscarepodcast.libsyn.com/rss

def main():
    print(f"{col.Fore.BLUE}Welcome to the AllCasts App!{col.Fore.RESET}")
    pod_url = pyip.inputURL(prompt='Please enter the URL of the podcast you want to download: ')
    download_dir = pyip.inputFilepath(prompt='Please enter the directory you want to download the podcast to [leave blank for current dir]: ', blank=True)
    if download_dir == '' or download_dir == '.':
        # set to current working directory
        download_dir = path.abspath('.')

    print(f"Downloading all podcasts from {pod_url} to {download_dir}")


    # download the podcast
    download_all_podcasts(pod_url, download_dir)
    


if __name__ == '__main__':
    main()