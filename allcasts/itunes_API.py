''' itunes_API.py

	This file contains the functions that interact with the iTunes API for searching for podcasts.	
'''

import urllib.request
import json
import os

class ItunesAPI():
	'''
	Class containing methods for searching the iTunes API for podcasts
	'''

	def podcast_search(query: str, limit: int = 10):
		'''
		search for a podcast by name and return a cleaned dictionary of the results
		podcasts[index]['name']
		podcasts[index]['url']
		podcasts[index]['description']
		'''
		with urllib.request.urlopen(f"https://itunes.apple.com/search?term={query}&limit={limit}&entity=podcast") as response:
			api_response = json.loads(response.read())['results']
		return api_response

	def format_itunes_response(api_response: list):
		'''format the response from the iTunes API into a list of dictionaries
		returns a list of dictionaries with the following keys:
			name, url
		'''
		formatted_podcasts = []
		for podcast in api_response['results']:
			formatted_podcasts.append({
				'name': podcast['collectionName'],
				'url': podcast['feedUrl'],
			})
		return formatted_podcasts

	

