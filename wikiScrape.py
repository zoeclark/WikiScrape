



from bs4 import BeautifulSoup
import urllib
import requests
from collections import defaultdict
import sys



def buzzArticle (url, n, oneGram, bigrams, d, depth, parent,  counters, onePar = False, ): 
	"""
	Method takes in the url of a seed wikipedia page as a string, the total recursion level n (both set by user), in addition to 3 dictionaries 
	(1grams, 2grams, words), the current level of recursion (depth), prev tracker ('parent', an instance of the Word), and counters for the 
	total number of pages and total number of 'needs ciation' tags. If the default 
	boolean 'onePar' == True, the algorithm only reads the first paragraph of text, not the whole article. The method fills in each dictionary 
	by reading all links on the seed wikipage, going to all these links, reading them and so on,  
	a until the depth of recurssion equals n. 
	""" 
	if len(sys.argv) == 4:
		if sys.argv[3] == 'frist paragraph':
			onePar = True

	curr = Word(url.replace("https://en.wikipedia.org", ""), parent)
	if depth < n: 
		queue = []	
		r = urllib.urlopen(url).read()
		soup = BeautifulSoup(r, "lxml")  
		if onePar == True:
			txt = soup.find('p') # for the the first paragraph 
		else:
			txt = soup.find_all('p') #for every paragraph 
		for p in txt:
			for a in p.find_all('a') : #for every a tag in every paragrah 
				try: 
					if a['href'][6:] == 'Wikipedia:Citation_needed':
							counters[1] += 1
					elif a['href'][0] != '#' and a['href'][6:]!= 'Wikipedia:Citing_sources' and a['href'][6:14]!= 'Help:IPA': #If I encouter any more types of URLS I don't want, I'll save them all in a STOP list 
						counters[0] += 1

						if oneGram [ a['href'] ] == 0: # if new --> into queue
							queue.append(a['href'])						
						print  "reading", a['href'], "from", curr.handle
						oneGram [a['href'] ] += 1
						thisWord = Word(a['href'], curr)
						d[a['href']][thisWord] += 1
						bigrams [tuple([ a['href'], curr.handle ])   ] += 1  #bigrams 				
				except KeyError: #rare, seems to occour when the page has a link to itself  
					print "KEY ERROR on ", url
		if n - (depth + 1) != 0 : #if the page is not not a leaf, move to its children 
			for wikiTag in queue:
				if wikiTag[:5] == '/wiki': # if the tag is a wikipedia page. Occasionaly links lead out of wikipedia, typically to wikiDictionary. Log out-of-wiki links in dictionary, but don't visit
						print "going to", wikiTag
						buzzArticle('https://en.wikipedia.org' + wikiTag, n, oneGram, bigrams, d,  depth + 1,  curr, counters) #update recurion level 

def returnBuzzwords(dictionary):
	"""
	method takes in dictionary mapping wiki tag handles to their frequency of occourance, sorts the dictionary by frequency, and returns
	the highest 50 frequencies. 
	"""
	print "BUZZWORDS: 50 most frequent associated wiki URLS:"  
	for i, v in enumerate(sorted(dictionary.items(), key = lambda x: x[1], reverse = True)):
		print v[0], "occorances:", v[1]  
		if i == 50:
			break 

def returnPaths(bigrams, d, wikiTag): 
	"""
	method takes in a dictionary of "bigrams" (WikiTag/ parent WikiTag pairs), a double dictionary mapping wikiTags to word instances
	to frequencies, and the seed wiki url. The method takes the first 50 "bigrams" with the highest frequencies. If the bigram doesn't
	represent a full path, a path starting with the seed URL, this method uses the double dictionary to look up the most likely path back to
	the seed URL. 
	"""

	for i, v in enumerate(sorted(bigrams.items(), key = lambda x: x[1], reverse = True)): #for the 50 most prevelant wikiURL/ WikiParent pairs 
		allPaths = []
		pair = []
		pair.append(v[0][0])
		pair.append (v[0][1]) 
		allPaths.append(pair)
		tag = v[0][1]  #second value in the bigram tupple (a wikiURL)
		if tag != wikiTag: # if the bigram is not a complete path 
			for a, b in enumerate(sorted(d[tag].items(), key = lambda x: x[1], reverse = True)): #for the 5 most prevlant word instances for that second value
				thisPath = []
				thisPath.append(v[0][0])
				thisPath.append(v[0][1])
				currWord = b[0]	 #word instance  
				while currWord.handle != wikiTag:
					thisPath.append(currWord.parent.handle)
					currWord = currWord.parent 
				allPaths.append(thisPath)
			if a == 5: 
				break 
		longest = pair  
		for path in allPaths:
			if len(path) > len(longest): #I made a design choice to take the longest path of the best 5 possible paths back from the bigram. I discuss this decision in my README. 
				longest = path
		print '\n' + 'Suggested Path (score = '+ str(v[1]),')' 
		stringPath = ''

		for wiki in longest[::-1]: 
			if len(stringPath) == 0:
				stringPath = stringPath + wiki
			else:
				stringPath = stringPath + '-->' + wiki
		
		print stringPath
	
		if i == 50:
			break


class Word:
	def __init__(self, handle, parent): 
		"""
		The word class allows me to map wiki urls to word instances. Unlike wiki Urls, which have multiple identical instances, 
		word instances are unique, and all word instances know their parents, allowing me to trace their path back to the seed
		URL.  
		"""

		self.handle = handle #string representation the a's 'href' attribute eg /wiki/einstien 
		self.parent = parent


if __name__ == "__main__" :
	oneGram = defaultdict(int)
	bigrams = defaultdict(int) 
	d =  defaultdict(lambda:defaultdict(int)) #dict mapping wikiTags to word instances to frequencies 
	depth = 0
	url = sys.argv[1]
	n = int(sys.argv[2])
	if len(sys.argv) == 4:
		if sys.argv[3] == 'frist paragraph':
			onePar = True
		else: #incorrect input
			print "to run the application on just the first paragraph, type <first paragraph> after the wikipage and recursion level in the terminal"  
	wikiTag =  url.replace("https://en.wikipedia.org", "")
	parent = Word(wikiTag, None)
	counters = []
	counters.append(0)
	counters.append(0) 
	buzzArticle(url, n, oneGram, bigrams, d, depth, parent, counters) 
	returnBuzzwords(oneGram) 
	returnPaths(bigrams, d, wikiTag) 
	print counters[1], "pages need citation out of a total of ", counters[0], "pages visited."