# запуск: FeaturesExtractor.py образец результат_для_проверки output_file
# -*- coding: utf-8 -*-

import os
import random
import sys

partOfSpeechFeatures = []
linksFeatures = []
#doubleLinkFeatures = []
#bigrammFeatures = []
slotsList = []
slotsFeatures = []
linksStatistics = {}
doubleSlotsFeatures = []

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
	
def getSlot(_str):
	global slotsList
	global slotsFeatures
	list = _str.split('\t')
	if list[3] not in slotsList:
		slotsFeatures.append("slot" + str(len(slotsList)))
		slotsList.append(list[3])
		return slotsFeatures[-1]
	else:
		return slotsFeatures[slotsList.index(list[3])]

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
	
def extractDoubleLinks(partsOfSpeech, prevs):
	temp = ["ROOT"]
	temp.extend(partsOfSpeech)
	
	index = 0
	doubleLinks = []
	for prev in prevs:
		index += 1
		if prev == 0:
			continue
		doubleLinks.append(temp[prevs[prev - 1]] + '_' + temp[prev] + '_' + temp[index])
		
	return doubleLinks
	
def extractDoubleSlots(slots, prevs):
	temp = ["Slot_ROOT"]
	temp.extend(slots)
	
	result = []
	index = 0
	for prev in prevs:
		index += 1
		if prev == 0:
			continue
		result.append(temp[prev] + "_" + temp[index])
	
	return result

def addLinksFeatures(partsOfSpeech, prevs, slots):
	#link features
	links = extractLinks(partsOfSpeech, prevs)
	global linksFeatures
	for link in links:
		if link not in linksFeatures:
			linksFeatures.append(link)
			linksStatistics[link] = 1
		else:
			linksStatistics[link] += 1
	#double links features
	'''
	doubleLinks = extractDoubleLinks(partsOfSpeech, prevs)
	global doubleLinkFeatures
	for i in doubleLinks:
		if i not in doubleLinkFeatures:
			doubleLinkFeatures.append(i)
	'''
	
	#double slot features
	doubleSlots = extractDoubleSlots(slots, prevs)
	global doubleSlotsFeatures
	for i in doubleSlots:
		if i not in doubleSlotsFeatures:
			doubleSlotsFeatures.append(i)

'''
def addBigrammFeatures(partsOfSpeech):
	global bigrammFeatures
	
	prev = "ROOT"
	for partOfSpeech in partsOfSpeech:
		feature = "BI_" + prev + "_" + partOfSpeech
		prev = partOfSpeech
		
		if feature not in bigrammFeatures:
			bigrammFeatures.append(feature)
'''

# строим список фичей
def buildFeatuesList(inputFile):
	partsOfSpeech = []
	prevs = []
	slots = []
	
	while True:
		str = inputFile.readline()
		
		partOfSpeech = getParchOfSpeech(str)
		if partOfSpeech == 'NONE':
			addLinksFeatures(partsOfSpeech, prevs, slots)
			#addBigrammFeatures(partsOfSpeech)
			
			partsOfSpeech = []
			prevs = []
			slots = []
		else:
			partsOfSpeech.append(partOfSpeech)
			prevs.append(getPrev(str))
			slot = getSlot(str)
			slots.append(slot)
		
		if str == '':
			break
		
		addPartOfSpeech(getParchOfSpeech(str))

# prob - процент предложений, который берем
def dumpFeatures(inputFile, label, prob, outputFile):
	while True:
		_str = ''
		partsOfSpeech = []
		prevs = []
		slots = []
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
				slots.append(getSlot(_str))
		
		if random.randrange(10) < prob:
			sentence = []
			sentence.extend([0] * len(partOfSpeechFeatures))
			sentence.extend([0] * len(linksFeatures))
			sentence.extend([0] * len(slotsFeatures))
			#sentence.extend([0] * len(bigrammFeatures))
			#sentence.extend([0] * len(doubleLinkFeatures))
			sentence.extend([0] * len(doubleSlotsFeatures))
			
			for i in partsOfSpeech:
				sentence[partOfSpeechFeatures.index(i)] += 1

			for i in slots:
				sentence[len(partOfSpeechFeatures)+len(linksFeatures)+slotsFeatures.index(i)] += 1

			doubleSlots = extractDoubleSlots(slots, prevs)
			for i in doubleSlots:
				sentence[len(partOfSpeechFeatures)+len(linksFeatures)+len(slotsFeatures)+doubleSlotsFeatures.index(i)] += 1
				
			'''
			prev = "ROOT"
			for partOfSpeech in partsOfSpeech:
				feature = "BI_" + prev + "_" + partOfSpeech
				prev = partOfSpeech
				sentence[len(partOfSpeechFeatures)+len(linksFeatures)+bigrammFeatures.index(feature)] += 1
			'''
				
			links =	extractLinks(partsOfSpeech, prevs)
			for i in links:
				sentence[len(partOfSpeechFeatures)+linksFeatures.index(i)] += 1
			
			'''
			doubleLinks = extractDoubleLinks(partsOfSpeech, prevs)
			for i in doubleLinks:
				sentence[len(partOfSpeechFeatures)+len(linksFeatures)+len(slotsFeatures)+doubleLinkFeatures.index(i)] += 1
			'''
			
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
			print("Slot features:\n" + str(slotsFeatures))
			print("Slot list:\n" + str(slotsList))
			#print("Bigramm features:\n" + str(bigrammFeatures))
			#print("Double links list size:\n" + str(len(doubleLinkFeatures)))
			#print("Double links list:\n" + str(doubleLinkFeatures))
			print("Double slots list size:\n" + str(len(doubleSlotsFeatures)))
			print("Double slots list:\n" + str(doubleSlotsFeatures))
			
			import operator
			sorted_x = sorted(linksStatistics.items(), key=operator.itemgetter(1))
			print("Links features statistics:\n" + str(sorted_x))
			
			maltUsualFile.seek(0)
			maltNullFile.seek(0)
			
			for i in partOfSpeechFeatures:
				outputFile.write(i + ",")
			for i in linksFeatures:
				outputFile.write(i + ",")
			for i in slotsFeatures:
				outputFile.write(i + ",")
			for i in doubleSlotsFeatures:
				outputFile.write(i + ",")
			#for i in bigrammFeatures:
			#	outputFile.write(i + ",")
			outputFile.write("label\n")
			
			dumpFeatures(maltUsualFile, 0, 2, outputFile)
			dumpFeatures(maltNullFile, 1, 100, outputFile)
