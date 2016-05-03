# -*- coding: utf-8 -*-

#Export to MaltTAB data format
import os
import random
import sys
from xml.dom.minidom import *

#globals
rootPath = "c:\SyntUp\SynTagRus"
version = '3'
prepath = 'export\\' + version + '\\'
blackList = ( 'structure_editor' )
trainFile = open( prepath + 'train.txt', 'w', encoding='utf8' )
testFile = open( prepath + 'test.txt', 'w', encoding='utf8' )
nullOutputFile = open( prepath + '\\null.txt', 'w', encoding='utf8' )
logFile = open( prepath + '\\export_log.txt', 'w', encoding='utf8' )

def isNullWord(word):
	return word.hasAttribute( "NODETYPE" ) and word.getAttribute( "NODETYPE" ) == "FANTOM"

#Проверяем является ли предложение нулевым
def isNullSentence(sentence):
	for word in sentence.getElementsByTagName( "W" ):
		#Обрабатываем нулевые вершины
		if isNullWord(word):
			return True
	return False
	
#Атрибуты слова
def convertAttributes(word):
	str = word.getAttribute('FEAT')
	return str.replace(' ', '.')
	
#Получаем предка слова
def convertParent(word):
	if word.getAttribute('DOM') == '_root':
		return '0'
	else: 
		return word.getAttribute('DOM')

#http://stp.lingfil.uu.se/~nivre/docs/Dialog.pdf
#deprel - тип связи
def convertDeprel(word):
	if word.hasAttribute('LINK'):
		return word.getAttribute('LINK')
	elif word.getAttribute('DOM') == '_root':
		return "#root"
	else:
		return "#Unknown"

#Обрабатываем файл с синт. разборами
def processTgtFile(filePath):
	document = parse( filePath )
	for documentBody in document.getElementsByTagName( "body" ):
		for sentence in documentBody.getElementsByTagName( "S" ):
			outF = trainFile
			#делим выборку на 30% test и 70% train
			if random.randrange(10) < 3:
				outF = testFile
		
			if isNullSentence(sentence):
				outF = nullOutputFile
				logFile.write("Null sentence id: " + str(sentence.getAttribute('ID'))+'\n')
			
			wordIndex = 0
			for word in sentence.getElementsByTagName( "W" ):
				wordText = ''
				if isNullWord(word):
					wordText = 'NULL'
				else:
					wordText = word.firstChild.nodeValue
			
				outF.write(wordText + '\t' + convertAttributes(word) + '\t' + convertParent(word) 
				+ '\t' + convertDeprel(word) + '\n')
				
			
			#Separate sentences
			outF.write('\n')

#Iteration dir
for dir in os.listdir( rootPath ):
	if os.path.isdir( os.path.join( rootPath, dir ) ) and not( dir in blackList ): #and dir == '2004':
		print( dir )
		logFile.write( "!!!!!!!!!!!  DIR:   " + os.path.join( rootPath, dir ) + "   !!!!!!!!!!!!!!!\n" )
		
		for file in os.listdir( os.path.join( rootPath, dir ) ):
			if file.endswith( ".tgt" ):
				logFile.write( "!!!!  FILE:   " + os.path.join( rootPath, dir, file ) + "   !!!!\n" )
				processTgtFile( os.path.join( rootPath, dir, file ) )
				logFile.write( "\n" )
				
		logFile.write( "\n" )
