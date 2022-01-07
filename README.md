# allcasts 📻 🗃

[![PyPI version](https://badge.fury.io/py/allcasts.svg)](https://pypi.org/project/allcasts/)

A Python package for downloading all available episodes from a podcast RSS feed. Useful for making private archives of your favourite podcasts.

![Demonstration GIF](https://github.com/illegalbyte/allcasts/blob/ea62a2e13a420b44336ac2100023eae7dca69d2a/img/0.1.16_example.gif?raw=true)

## Installation

`pip install allcasts`

## Usage

### Command line utility

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

### As a Python module

allcasts is a Python module that can be imported and used in your own Python code too!

```python
from allcasts import AllCasts

AllCasts.download_all('https://atp.fm/rss', '/Users/lewis/Documents/Python-Projects/allcasts')
```

### Limitations

- Private Patreon RSS feeds are not currently supported due to their strange DRM measures. 

## Todo

- [ ] Add support for downloading multiple podcasts at once.
- [ ] Add support for command line arguments.
- [ ] Add itunes API support to search for podcasts and select the correct feed.

<!-- https://realpython.com/pypi-publish-python-package/ -->
<!-- $ bumpversion --current-version 1.0.0 minor setup.py reader/__init__.py -->
<!-- https://python-packaging.readthedocs.io/en/latest/minimal.html -->
