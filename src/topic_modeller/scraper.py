from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd

# https://cse.google.com/cse/setup/basic?cx=015147876388115285117:jawckofl0l3
# https://blog.expertrec.com/google-custom-search-json-api-simplified/

qry = "https://www.googleapis.com/customsearch/v1?key={KEY}&cx={ENGINE_ID}&q={KEYWORD}".format(
	KEY="AIzaSyBtFKaXXRAQLj2iifoN71Nj1-3tkVkdBSg"
	, ENGINE_ID="015147876388115285117:jawckofl0l3"
	, KEYWORD="brexit")


def getArticleText(soup):
    para_list = soup.find_all('p')
    paragraphs = []
    for para in para_list:
        paragraphs.append(para.getText().split('\n')[0])
    doc = " ".join(paragraphs)
    return doc

def getArticleTime(soup):
	time = soup.find('time', attrs={"itemprop":"datePublished"})
	return time['datetime']


docs = []
time = []
urls = pd.read_csv('./guardian_urls.txt', header=None)

for url in urls[0]:
	try:
	    page = urllib.request.urlopen(url)
	    soup = BeautifulSoup(page, 'html.parser')

	    docs.append(getArticleText(soup))
	    time.append(getArticleTime(soup))

	except Exception as e:
		print(e)


#pd.DataFrame({'docs':docs, 'dates':time}).to_csv('documents.txt', sep =',', index=False)

with open('content2.txt', 'w') as f:
    for doc in docs:
        f.write(doc+"\n")

