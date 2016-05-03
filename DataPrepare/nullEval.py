# запуск: nullEval.py образец результат_для_проверки output_file
# -*- coding: utf-8 -*-

import os
import random
import sys
from xml.dom.minidom import *

def readPrecise(preciseNullFile):
	isEnd = False
	prev = [-1]
	isNull = []
	
	while True:
		s = preciseNullFile.readline()
		if s == '':
			isEnd = True
			break
		
		parts = s.split('\t')
		
		if (len(parts) < 4):
			break
		
		isNull.append(parts[0] == 'NULL')
		prev.append(int(parts[2]))
	
	return isEnd, prev, isNull

def readTest(testNullFile):
	prev = [-1]

	while True:
		s = testNullFile.readline()
		
		parts = s.split('\t')
		
		if (len(parts) < 4):
			break
		
		prev.append(int(parts[2]))
	
	return prev

outputFile = open(sys.argv[3], 'w', encoding='utf8')
total = 0
good = 0
total2 = 0
with open(sys.argv[1], 'r', encoding='utf8') as preciseNullFile:
	with open(sys.argv[2], 'r', encoding='utf8') as testNullFile:
		while True:
			isEnd, precisePrev, preciseIsNull = readPrecise(preciseNullFile)
			
			testPrev = readTest(testNullFile)
			
			#build map
			testToPrecise = {0:0}
			index = 0
			testIndex = 0 
			for isNull in preciseIsNull:
				index += 1
				if not isNull:
					testIndex += 1
					testToPrecise[testIndex] = index
					
			total2 += len(precisePrev) - 1
			
			failCount = 0
			
			#count good links number
			testIndex = 0
			for prev in testPrev:
				if prev < 0:
					continue
				
				testIndex += 1
				
				total += 1
				
				# лево: предок в тестовом дереве + отображение в точное дерево
				# право: берем индекс в точном дереве и предок в точном дереве
				if testToPrecise[prev] == precisePrev[testToPrecise[testIndex]]:
					good += 1
				else:
					failCount += 1
			
			outputFile.write(str(failCount) + '\n')
			
			# Останавливаем когда нужно
			if isEnd:
				break
			
outputFile.write( str(good) + " " + str(total) + " " + str(total2) + " " + str(1.0*good/total) + " " + str(1.0*good/total2) + '\n' )
