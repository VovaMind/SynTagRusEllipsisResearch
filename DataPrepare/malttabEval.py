# запуск: malttabEval.py образец результат_для_проверки output_file
# -*- coding: utf-8 -*-

#Export to MaltTAB data format
import os
import random
import sys
from xml.dom.minidom import *

good = 0
total = 0

goodSentences = 0
totalSentences = 0
failed = False

def check(s1, s2):
	global failed
	global totalSentences
	global goodSentences
	
	list1 = s1.split('\t')
	list2 = s2.split('\t')
	
	if (len(list1) < 4 or len(list2) < 4):
		totalSentences += 1
		if not failed:
			goodSentences += 1
		failed = False
		return
	
	global total
	total += 1
	
	if (list1[2] == list2[2]):
		global good
		good += 1
	else:
		failed = True

total = 0
with open(sys.argv[1], 'r', encoding='utf8') as preciseFile:
	with open(sys.argv[2], 'r', encoding='utf8') as testFile:
		while (True):
			s1 = preciseFile.readline()
			if s1 == '':
				break
				
			s2 = testFile.readline()
			assert(s2 != '')

			check(s1, s2)

outputFile = open(sys.argv[3], 'w', encoding='utf8')
outputFile.write('Links eval:\n')
outputFile.write( str(good) + " " + str(total) + " " + str(1.0*good/total) + '\n' )
outputFile.write('Sentences eval:\n')
outputFile.write( str(goodSentences) + " " + str(totalSentences) + " " + str(1.0*goodSentences/totalSentences) + '\n' )
