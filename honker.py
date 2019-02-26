# Python script to make a readable PDF of websites
# files for later offline reading and annotation.
# This is simlar to browsers' "Reading View" of a website.
# Which started with Instapaper, the Arc90 Project, and 
# Safari version 5:
#   https://www.ctrl.blog/entry/browser-reading-mode-parsers#
#   http://ejucovy.github.io/readability/
#   https://en.wikipedia.org/wiki/Readability_(service)
#   https://github.com/masukomi/arc90-readability
# Quite a few are available today, after briefly testing
# a few, the Goose article extractor worked the best for me.
#   https://github.com/goose3/goose3 
#   https://goose3.readthedocs.io/en/latest/code.html#article 
#

#sample English article
#url='http://koreabizwire.com/drones-becoming-more-and-more-integral-to-everyday-life/88550'
#sample Korean article
#url='http://ddaily.co.kr/news/article.html?no=165110'

# TODO: 
# Strip away unwanted characters based on their Unicode languge range:
# Hangul Syllable Unicode range: AC00 — D7AF 
# English, sort of: 0020 - 03FF
# Example: this site has some unexpected Hebrew characters:
# 	https://i-hls.com/archives/82236
# Also, mid-line dot character not in my font
#

import time
import sys
import csv
from goose3 import Goose
from goose3.text import StopWordsKorean
import langid

def stripnews( string ):
  return string.strip("., ")

def striptitle( title ):
  return ''.join( c for c in title if  c not in '[:]' )
          
def prepstr( thing, default ):
  if thing == None:
    return default
  if len(thing) == 0:
    return default
  else:
    return stripnews(thing).split('\n')[0]

def preplist( things, default ):
  if things == None:
    return default
  if len(things) == 0:
    return default
  else:
    return stripnews(", ".join(things))

def printthings( things, fp ):
  if things == None:
    print("None", file=fp)
    return
  if len(things) == 0:
    print("None", file=fp)
    return
  else:
    for i, thing in enumerate(things, start=0):
      if "http" in thing:
        if    "jpg" in thing \
        or "jpeg" in thing \
        or  "png" in thing:
          print("![image",str(i).zfill(3),"](",thing,")", sep='', file=fp)
        else:
          print("[",thing,"](",thing,")", sep='', file=fp)

urls=[]
if len(sys.argv) < 2:
  baseno=0
else:
  baseno=sys.argv[1]

#fname=sys.argv[1]
#baseno=sys.argv[2]
#with open(fname) as f:
#  reader=csv.reader(f)
#  for line in reader:
#  urls.append(line[0])
#f.close()

for line in csv.reader(iter(sys.stdin.readline, '')):
  urls.append(line[0])
#print(len(urls))

for iu, url in enumerate(urls, start=int(baseno)):
  #if iu > 5:
  #  continue

  ofname="news"+str(iu).zfill(3)+".md"
  of=open(ofname,'w')
  print(ofname,url,sep='\t')

  g = Goose({'stopwords_class':StopWordsKorean})
  #g = Goose()
  article = g.extract(url=url)

  if False:
    print("cleaned text:")
    print("  type: ", type(article.cleaned_text))
    print("  text: ", article.cleaned_text[:50])
    print("guessed language: ", langid.classify(article.cleaned_text))
    print("authors:")
    print("  type: ", type(article.authors))
    print("values: ", article.authors)
    print("top image:")
    print("  type: ", type(article.top_image), sep='\t')
    print("values: ", article.top_image)
    print("typeof article_links:", type(article.links), sep='\t')
    print("links:")
    print("  type: ", type(article.links))
    print("values: ", article.links)
    print("tags:")
    print("  type: ", type(article.tags))
    print("  tags: ", article.tags)
    print("meta keywords:")
    print("  type: ", type(article.meta_keywords))
    print("  meta: ", article.meta_keywords)

  if True:
    print("---", file=of)
    print("title:", prepstr(striptitle(article.title), "No Title Available"), sep='\t', file=of)
    print("author:", preplist(article.authors, "No Author Information"), sep='\t', file=of)
    print("date:", prepstr(article.publish_date, "Published Date Missing"), sep='\t', file=of)
    print("pagelink:", prepstr(article.final_url, "URL Not Available"), sep='\t', file=of)
    print("language:", prepstr(article.meta_lang, "Language Information Not Available"), sep='\t', file=of)
    print("pagetags:", preplist(article.tags, "No Tags"), sep='\t', file=of)
    print("metakeys:", prepstr(article.meta_keywords, "No Keywords"), sep='\t', file=of)
    print("---", file=of)
    print(file=of)
    print(article.cleaned_text, file=of)
    printthings(article.top_image, of)
    print(file=of)
    print("### Links and Images", file=of)
    print(file=of)
    printthings(article.links, of)
    print(file=of)
    print("### Metadata", file=of)

  of.close()
