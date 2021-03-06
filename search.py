import urllib2
import simplejson
import re
import requests
from bs4 import BeautifulSoup
from random import choice

scraped_text = list()
words = list()

output_line = list()

real_words_cleaned  = list()


big_list_of_words = list()

real_words_file = open("sowpods.txt")
real_words = real_words_file.readlines()
real_words_file.close()


for line in real_words:
	line = line.strip()
	real_words_cleaned.append(line)


#function to use if we want to control size of string
# from bs4 import SoupStrainer
# 
# only_a_tags = SoupStrainer("a")
# 
# only_tags_with_id_link2 = SoupStrainer(id="link2")
# 
# def is_short_string(string):
#     return len(string) < 10
# 
# only_short_strings = SoupStrainer(text=is_short_string)


											# The request also includes the userip parameter which provides the end
											# user's IP address. Doing so will help distinguish this legitimate
											# server-side traffic from traffic which doesn't come from an end-user.



id = "hotdog"  								# dynamic id from site in a post request
url = ('https://ajax.googleapis.com/ajax/services/search/web'
       '?v=1.0&q='+ id + '&userip=USERS-IP-ADDRESS')

request = urllib2.Request(url, None, {'Referer': "www.google.com" })
response = urllib2.urlopen(request)  # opening url

    							# Process the JSON string.
results = simplejson.load(response)
results = results["responseData"]
results = results['cursor']
nofResults = (results["resultCount"])
										# set a variable for search result pagination
nom = long(nofResults.replace(",", ""))/ 10000

print "Results searched...." ,nom
results = results["moreResultsUrl"]
#print results

								#results = results['resultCount']

								#regex to add number to results
split = re.split("start=0", results)
newurl= split[0] + "start=" + str(nom) +split[1]
print "found!!!"+ newurl 

r = requests.get(newurl)
								# print r.status_code
								# print r.headers['content-type']

r= r.text
soup = BeautifulSoup(r)
all = []
for link in soup.find_all("a"):
	all.append(link.get("href"))
listOfUrls= []

for s in all:					#iterate through the document and extract links
	if re.findall("/url?", s):

                split1 = re.split("&", s)
                split2 =re.split("=", split1[0])
                deathlinks=[]
                sp =(split2[1]).split("//n")
                #print sp[0]
                
                				# list of lists
                listOfUrls.append(sp[0])

								#random url selected
deathUrl = choice(listOfUrls)
								#printing the selected url
print "I am chosen to die!" + deathUrl

								#open urls and parse 
death= urllib2.urlopen(deathUrl)
death = death.read()

deathSoup = BeautifulSoup(death)
#forContext = deathSoup.get_text()

#print forContext
# a different HTML parse function using stripped string to remove white space



for string in deathSoup.stripped_strings:
							 								#context free variable from site
	tocontextfree = (string)
	scraped_text.append(tocontextfree)

#	print tocontextfree


for lines in scraped_text:
	lines = lines.strip()
	whatever = lines.split(" ")
	
	for word in whatever:
		word = word.lower()
		word = word.encode('ascii', 'ignore')
		big_list_of_words.append(word)

for word in big_list_of_words:
	if word in real_words_cleaned:
		output_line.append(word)

print output_line
