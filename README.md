# allcasts 📻 🗃

[![PyPI version](https://badge.fury.io/py/allcasts.svg)](https://pypi.org/project/allcasts/)

A Python package for downloading all available episodes from a podcast RSS feed. Useful for making private archives of your favourite podcasts.

![Demonstration GIF](https://github.com/illegalbyte/allcasts/blob/ea62a2e13a420b44336ac2100023eae7dca69d2a/img/0.1.16_example.gif?raw=true)

## Installation

`pip install allcasts`

## Usage

### Command Line: Interactive Mode

From your terminal run `allcasts` which will kindly ask you for the an RSS feed's URL and download all available episodes for that podcast.

```shell
$ allcasts
==========================================================
 ========= Welcome to the AllCasts App! ========
==========================================================
Please enter the URL of the podcast feed you want to download: https://atp.fm/rss
Please enter the directory you want to download the podcast to [leave blank for current dir]: 
Downloading all podcasts from https://atp.fm/rss to /Users/lewis/Documents/Python-Projects/allcasts
Downloading https://traffic.libsyn.com/atpfm/atp464.mp3
[............................................................................................]
🎧 Downloaded 464: Monks at Drafting Tables
Downloading https://traffic.libsyn.com/atpfm/atp463.mp3
[............................................................................................]
🎧 Downloaded 463: No Indication of Progress
Downloading https://traffic.libsyn.com/atpfm/atp462.mp3
[............................................................................................]
🎧 Downloaded 462: Xcode X
Downloading https://traffic.libsyn.com/atpfm/atp461.mp3
[...........                                                                                 ]
```

### Command Line: Arguments

Allcasts supports a variety of command line arguments. To display help message below use `allcasts -h`

```bash
usage: allcasts.py [-h] (-f <URL> | -i <FILE>) [-d <DIRECTORY>] [-t] [-s <NUMBER>] [-e <NUMBER>] [-a] [-n <NUMBER>] [-l] [-v]

A friendly command line podcast downloader - supports downloading entire feeds, individual episodes, and a range of episodes

optional arguments:
  -h, --help            show this help message and exit
  -f <URL>, --feed <URL>
                        the url of the podcast feed
  -i <FILE>, --input <FILE>
                        the input file containing a list of podcast feeds
  -d <DIRECTORY>, --directory <DIRECTORY>
                        the directory to save the podcast episodes
  -t, --transcribe      transcribe the podcast episodes to text
  -s <NUMBER>, --start <NUMBER>
                        the number of the first episode to download
  -e <NUMBER>, --end <NUMBER>
                        the number of the last episode to download
  -a, --all             download all episodes
  -n <NUMBER>, --number <NUMBER>
                        download a specific episode
  -l, --latest          download the latest episode
  -v, --version         display the version number
```

#### Example Commands

* **Download episodes 100 to 120**

```bash
allcasts -f "https://atp.fm/rss" -s 100 -e 120
```

* **Download all episodes of a podcast**

```bash
allcasts -f "https://atp.fm/rss" -a
```

* **Download episode 200**

```bash
allcasts -f "https://atp.fm/rss" -n 100
```

* **Download a list of RSS feeds**

```bash
allcasts -i "podcast_feeds.txt"
```

* **Transcribe downloaded episodes to a txt file for keyword searching**

```bash
allcasts -f "https://atp.fm/rss" -t
```

### As a Python module

allcasts is a Python module that can be imported and used in your own Python code too!

```python
from allcasts import AllCasts

AllCasts.download_all('https://atp.fm/rss', '/Users/lewis/Documents/Python-Projects/allcasts')
```

### Limitations

* Private Patreon RSS feeds are not currently supported due to their strange DRM measures. 

## Todo

* [X] Add audio transcription using [speech_recognition module](https://github.com/Uberi/speech_recognition)
* [ ] Add support for private [Patreon RSS feeds](https://www.patreon.com/posts/podcast-feed-for-patrons-on-patreon)
* [X] Add support for downloading multiple podcasts at once.
* [X] Add support for command line arguments.
* [X] Add itunes API support to search for podcasts and select the correct feed.

<!-- https://realpython.com/pypi-publish-python-package/ -->
<!-- $ bumpversion --current-version 1.0.0 minor setup.py reader/__init__.py -->
<!-- https://python-packaging.readthedocs.io/en/latest/minimal.html -->
