# vocaberry - vocabulary program - web scraping


import urllib.request
import re
from bs4 import BeautifulSoup

site_url = 'http://www.vocabulary.com/dictionary/'

word = input('Enter Word: ')


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def suggestion(w, data):
	soup = BeautifulSoup(data, features="html.parser")
	suggestions = soup.find("ol", {"class":"suggestions"})
	# print(suggestions.find("li"))
	sug_word = suggestions.find("li")['word']
	print("Did you mean '", sug_word, "'?")
	find(sug_word)

def check_exist(word, data):
	soup = BeautifulSoup(data, features="html.parser")
	res = soup.find("div", {"class":"noresults"})
	return res

def extract_vocabulary(tag_search, data):
	if tag_search==None:
		soup = BeautifulSoup(data, features="html.parser")
		definition = soup.find("h3", {"class":"definition"}).get_text().strip()
		print(definition)
	else:
		start = tag_search.start()
		# end = start + 50

		# se = data[start:end]
		# print(se)

		end_scraping = re.search('<div class="adslot" id="dictionary-upper-ad"', data)
		s = end_scraping.start()
		# e = end_scraping.end()
		# mine = data[s:e]
		# print(mine)


		st = data[start:s]
		# print(st)

		scrap_start = re.search('class="short">', st)
		scrap_end = re.search('</p>', st)
		start = scrap_start.end()
		end = scrap_end.start()


		string = st[start:end]
		voc = cleanhtml(string)
		print(voc)


def find(word):
	search_url = site_url + urllib.parse.quote(word)

	raw_data = urllib.request.urlopen(search_url).read()
	data = raw_data.decode("utf-8")

	tag_search = re.search('<p class="short">', data)

	check = check_exist(word, data)
	if check!=None:
		print("Word not found!")
		suggestion(word, data)
	else:
		extract_vocabulary(tag_search, data)



find(word)