from __future__ import absolute_import
from __future__ import print_function
import six

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


def findDates(keyword):
    dates_with_sentences=''
    matches = datefinder.find_dates(keyword)
    for match in matches:
        sentencesWithDatesArray[sentence] = str(match)
        print(match)

    convertToJSON('output_data/dates.json', sentencesWithDatesArray)


def dumpToFile(fileName, data):
    f = open(fileName, 'w')
    f.write(data)
    f.close()


def convertToJSON(fileName, data):
    with open(fileName, 'w', encoding="utf8") as outfile:
        json.dump(data, outfile)


stoppath = "data/stoplists/SmartStoplist.txt"

# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath, 5, 3, 2)

# 2. run on RAKE on a given text
sample_file = io.open("data/chat.txt", 'r', encoding="iso-8859-1")
text = sample_file.read()

keywords = rake_object.run(text)

rake_object = rake.Rake(stoppath)

# 1. Split text into sentences
sentenceList = rake.split_sentences(text)

# generate candidate keywords
stopwords = rake.load_stop_words(stoppath)
stopwordpattern = rake.build_stop_word_regex(stoppath)
phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern, stopwords)

# calculate individual word scores
wordscores = rake.calculate_word_scores(phraseList)

# generate candidate keyword scores
keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)

# sort candidates by score to determine top-scoring keywords
sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
totalKeywords = len(sortedKeywords)

popularSentences = ''
popularKeywords = ''

for sentence in sentenceList:
    if sentence:
        findDates(sentence)

for keyword in keywords:
    popularKeywords += keyword[0] + '\n'
    for sentence in sentenceList:
        if keyword[0] in sentence:
            popularSentences += sentence + '\n'
dumpToFile('output_data/popular_sentences.txt', popularSentences)
dumpToFile('output_data/popular_keywords.txt', popularKeywords)
