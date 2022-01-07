#! python3

from _typeshed import Self
import pyinputplus as pyip
import colorama as col
import wget
import urllib
import xmltodict
from os import path
import os

# initialise colorama for Windows
col.init()

class AllCasts(Self):

    def download_podcast(url, directory, filename):
        '''
        download the podcast episode from the url and save it to the directory
        '''
        print(f"Downloading {url}")
        wget.download(url, out=directory, bar=wget.bar_thermometer)


    def download_all_podcasts(self, url, directory):
        '''
        download all podcasts from the url and save them to the directory
        '''
        self.create_directory(directory)
        XML = urllib.request.urlopen(url).read()
        podcast_dict = xmltodict.parse(XML)
        for item in podcast_dict['rss']['channel']['item']:
            podcast_title = item['title']
            file_name = f"{podcast_title}.mp3"
            self.download_podcast(item['enclosure']['@url'], directory, file_name)
            print(f"\n{col.Fore.GREEN}🎧 Downloaded {podcast_title}{col.Fore.RESET}")
        print(f"\n{col.Fore.BLUE}--> 🎉 All podcasts downloaded!{col.Fore.RESET}")


    def create_directory(directory):
        '''
        create the directory if it doesn't exist
        '''
        if not path.exists(directory):
            print(f"Creating directory {directory}")
            os.makedirs(directory)

    # test url:
    # https://redscarepodcast.libsyn.com/rss

def main():
    # welcome message
    print(f"{col.Fore.BLUE}Welcome to the AllCasts App!{col.Fore.RESET}")
    # prompt the user for the url
    pod_url = pyip.inputURL(prompt='Please enter the URL of the podcast you want to download: ')
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
