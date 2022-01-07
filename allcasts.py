#! python3

import pyinputplus as pyip
import colorama as col
import urllib.request
import xmltodict
from os import path

# initialise colorama for Windows
col.init()

def download_podcast(url, directory, filename):
    print(f"Downloading {url}")
    urllib.request.urlretrieve(url, path.join(directory, filename))
    urllib.request.urlretrieve()

def download_all_podcasts(url, directory):
    XML = urllib.request.urlopen(url).read()
    podcast_dict = xmltodict.parse(XML)
    for item in podcast_dict['rss']['channel']['item']:
        podcast_title = item['title']
        file_name = f"{podcast_title}.mp3"
        download_podcast(item['enclosure']['@url'], directory, file_name)


def main():
    print(f"{col.Fore.BLUE}Welcome to the AllCasts App!{col.Fore.RESET}")
    pod_url = pyip.inputURL(prompt='Please enter the URL of the podcast you want to download: ')
    download_dir = pyip.inputFilepath(prompt='Please enter the directory you want to download the podcast to: ')
    if download_dir == '' or download_dir == '.':
        # set to current working directory
        download_dir = path.abspath('.')

    print(f"Downloading all podcasts from {pod_url} to {download_dir}")


    # download the podcast
    download_all_podcasts(pod_url, download_dir)
    


if __name__ == '__main__':
    main()