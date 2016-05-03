# запуск: FeaturesExtractor.py образец результат_для_проверки output_file
# -*- coding: utf-8 -*-

import os
import random
import sys

partOfSpeechFeatures = []
linksFeatures = []
linksStatistics = {}

def getParchOfSpeech(str):
	list = str.split('\t')
	
	if len(list) < 4:
		return 'NONE'
	else:
		tmp = list[1]
		pos = tmp.find('.')
		if pos != -1:
			tmp = tmp[0:pos]
			
		return tmp
		
def getPrev(str):
	list = str.split('\t')
	return int(list[2])

def addPartOfSpeech(partOfSpeech):
	global partOfSpeechFeatures
	if partOfSpeech != 'NONE':
		if partOfSpeech not in partOfSpeechFeatures:
			partOfSpeechFeatures.append(partOfSpeech)
			
def extractLinks(partsOfSpeech, prevs):
	temp = ["ROOT"]
	temp.extend(partsOfSpeech)
	
	index = 0
	links = []
	for prev in prevs:
		index += 1
		links.append(temp[prev] + '_' + temp[index])
		
	return links
	
def addLinksFeatures(partsOfSpeech, prevs):
	links = extractLinks(partsOfSpeech, prevs)
	global linksFeatures
	for link in links:
		if link not in linksFeatures:
			linksFeatures.append(link)
			linksStatistics[link] = 1
		else:
			linksStatistics[link] += 1

# строим список фичей
def buildFeatuesList(inputFile):
	partsOfSpeech = []
	prevs = []
	
	while True:
		str = inputFile.readline()
		
		partOfSpeech = getParchOfSpeech(str)
		if partOfSpeech == 'NONE':
			addLinksFeatures(partsOfSpeech, prevs)
			
			partsOfSpeech = []
			prevs = []
		else:
			partsOfSpeech.append(partOfSpeech)
			prevs.append(getPrev(str))
		
		if str == '':
			break
		
		addPartOfSpeech(getParchOfSpeech(str))

# prob - процент предложений, который берем
def dumpFeatures(inputFile, label, prob, outputFile):
	while True:
		_str = ''
		partsOfSpeech = []
		prevs = []
		while True:
			_str = inputFile.readline()
			if _str == '':
				break
			
			partOfSpeech = getParchOfSpeech(_str)
			
			if (partOfSpeech == 'NONE'):
				break
			else:
				partsOfSpeech.append(partOfSpeech)
				prevs.append(getPrev(_str))
		
		if random.randrange(10) < prob:
			sentence = []
			sentence.extend([0] * len(partOfSpeechFeatures))
			sentence.extend([0] * len(linksFeatures))
			
			for i in partsOfSpeech:
				sentence[partOfSpeechFeatures.index(i)] += 1
				
			links =	extractLinks(partsOfSpeech, prevs)
			for i in links:
				sentence[len(partOfSpeechFeatures)+linksFeatures.index(i)] += 1
			
			for feature in sentence:
				outputFile.write(str(feature)+",")
			outputFile.write(str(label)+'\n')
			
		if _str == '':
			break

with open(sys.argv[1], 'r', encoding='utf8') as maltUsualFile:
	with open(sys.argv[2], 'r', encoding='utf8') as maltNullFile:
		with  open(sys.argv[3], 'w', encoding='utf8') as outputFile:
			buildFeatuesList(maltUsualFile)
			buildFeatuesList(maltNullFile)
			
			print("Part of speech tags:\n" + str(partOfSpeechFeatures))
			print("Links features:\n" + str(linksFeatures))
			
			import operator
			sorted_x = sorted(linksStatistics.items(), key=operator.itemgetter(1))
			print("Links features statistics:\n" + str(sorted_x))
			
			maltUsualFile.seek(0)
			maltNullFile.seek(0)
			
			for i in partOfSpeechFeatures:
				outputFile.write(i + ",")
			for i in linksFeatures:
				outputFile.write(i + ",")
			outputFile.write("label\n")
			
			dumpFeatures(maltUsualFile, 0, 1, outputFile)
			dumpFeatures(maltNullFile, 1, 100, outputFile)
