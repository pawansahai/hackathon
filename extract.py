from __future__ import absolute_import
from __future__ import print_function
import six
__author__ = 'a_medelyan'

import rake
import operator
import io

from datetime import datetime
import datefinder
import json

sentencesArray = {}
keywordsArray = {}
phrasesArray = {}
datesArray = {}
sentencesWithDatesArray = {}

def convertToJSON(fileName, data):
  with open(fileName, 'w', encoding="utf8") as outfile:
       json.dump(data, outfile)

def findDates(keyword):
   print("find date")
   matches = datefinder.find_dates(keyword)
   for match in matches:
       sentencesWithDatesArray[sentence] = str(match)
       print(match)

   convertToJSON('output_data/dates.json', sentencesWithDatesArray)

# EXAMPLE ONE - SIMPLE
stoppath = "data/stoplists/SmartStoplist.txt"

# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath, 5, 3, 4)

# 2. run on RAKE on a given text
sample_file = io.open("data/chat.txt", 'r',encoding="iso-8859-1")
text = sample_file.read()

keywords = rake_object.run(text)
convertToJSON('output_data/keywords.json', keywords)
# 3. print results
print("Keywords:", keywords)

print("----------")
# EXAMPLE TWO - BEHIND THE SCENES (from https://github.com/aneesha/RAKE/rake.py)

# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath)




# 1. Split text into sentences
sentenceList = rake.split_sentences(text)

for sentence in sentenceList:
    if sentence:
        print("Sentence:", sentence)
        findDates(sentence)

convertToJSON('output_data/sentences.json', sentenceList)

# generate candidate keywords
stopwords = rake.load_stop_words(stoppath)
stopwordpattern = rake.build_stop_word_regex(stoppath)
phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern, stopwords)
print("Phrases:", phraseList)
convertToJSON('output_data/phrases.json', phraseList)

# calculate individual word scores
wordscores = rake.calculate_word_scores(phraseList)

# generate candidate keyword scores
keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)
for candidate in keywordcandidates.keys():
    print("Candidate: ", candidate, ", score: ", keywordcandidates.get(candidate))
convertToJSON('output_data/candidates.json', keywordcandidates)

# sort candidates by score to determine top-scoring keywords
sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
totalKeywords = len(sortedKeywords)

# for example, you could just take the top third as the final keywords
for keyword in sortedKeywords[0:int(totalKeywords)]:
    print("Keyword: ", keyword[0], ", score: ", keyword[1])

print(rake_object.run(text))

for x in sentencesWithDatesArray:
  print(x)
  print(sentencesWithDatesArray[x])


