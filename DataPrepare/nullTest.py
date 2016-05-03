#Test for nulls in SynTagRus
import os
from xml.dom.minidom import *

#Const section
rootPath = "c:\SyntUp\SynTagRus"
blackList = ( 'structure_editor' )
logFile = open( 'log.txt', 'w' )
outputFile = open( 'output.txt', 'w' )

#statistics
dirsCount = 0
filesCount = 0
sentencesCount = 0
nullSentencesCount = 0
maxNullCount = 0
nullCountToSentencesCount = {}
partOfSpeechToNullsCount = {}
totalWordsCount = 0
totalWordsinNullSentencesCount = 0
oneNullSentencesStatistics = {}
twoNullsSentencesStatistics = {}
nonProjectiveCount = 0
nullAndNonProjectiveCount = 0
verbRootNullSentencesCount = 0
nullWithHintsCount = 0
hintSentencesCount = 0

#functions
def addToMap( map, value ):
	if value not in map:
		map[value] = 1
	else:
		map[value] += 1
		
class segment:
	def __init__( self, begin, end ):
		self.begin = min( begin, end )
		self.end = max( begin, end )
		
	def IsIntesect( self, seg ):
		intersectBegin = max( self.begin, seg.begin )
		intersectEnd = min( self.end, seg.end )
		
		return ( intersectBegin < intersectEnd ) and ( intersectBegin != self.begin or intersectEnd != self.end ) and ( intersectBegin != seg.begin or intersectEnd != seg.end )
		
def IsProjective( segments ):
	for s1 in segments:
		for s2 in segments:
			if s1.begin != s2.begin and s1.end != s2.end and s1.IsIntesect( s2 ):
				return False
	return True
				

def processTgtFile( filePath ):
	global filesCount
	global sentencesCount
	global nullSentencesCount
	global maxNullCount
	global nullCountToSentencesCount
	global partOfSpeechToNullsCount
	global totalWordsCount
	global totalWordsinNullSentencesCount
	global oneNullSentencesStatistics
	global twoNullsSentencesStatistics
	global nonProjectiveCount
	global nullAndNonProjectiveCount
	global verbRootNullSentencesCount
	global nullWithHintsCount
	global hintSentencesCount
	
	filesCount += 1
	
	logFile.write( filePath + "\n" )
	
	document = parse( filePath )
	for documentBody in document.getElementsByTagName( "body" ):
		for sentence in documentBody.getElementsByTagName( "S" ):
			sentencesCount += 1

			hasNulls = False
			nullsCount = 0
			sentenceWordsCount = 0
			partsOfSpeech = []
			segments = []
			lemmas = []
			for word in sentence.getElementsByTagName( "W" ):
				sentenceWordsCount += 1

				#Добавляем сегмент
				p1 = word.getAttribute( 'ID' )
				p2 = word.getAttribute( 'DOM' )

				if p2 == '_root':
					p2 = 0
					
				segments.append( segment( int( p1 ), int( p2 ) ) )

				#Обрабатываем нулевые вершины
				if word.hasAttribute( "NODETYPE" ) and word.getAttribute( "NODETYPE" ) == "FANTOM":
					#Простая статистика
					hasNulls = True
					nullsCount += 1
					
					#Нулевой глагол + корень
					if word.getAttribute( "DOM" ) == '_root' and word.getAttribute( "FEAT" ).find( "V" ) != -1:
						verbRootNullSentencesCount += 1
					
					#Обработка части речи
					feat = word.getAttribute( "FEAT" )
					
					substrLen = feat.find( " " )
					if substrLen == -1:
						substrLen = len( feat )
						
					partOfSpeech = feat[0:substrLen]
					partsOfSpeech.append( partOfSpeech )
					
					addToMap( partOfSpeechToNullsCount, partOfSpeech )
				else:
					lemmas.append( word.getAttribute( "LEMMA" ) )
					
			isFullHitSentence = True
			for word in sentence.getElementsByTagName( "W" ):
				if word.hasAttribute( "NODETYPE" ) and word.getAttribute( "NODETYPE" ) == "FANTOM":
					if word.getAttribute( "DOM" ) != '_root' and lemmas.count( word.getAttribute( "LEMMA" ) ) > 0:
						nullWithHintsCount += 1
					else:
						if word.getAttribute( "DOM" ) != '_root' or word.getAttribute( "FEAT" ).find( "V" ) == -1:
							isFullHitSentence = False
			
			if isFullHitSentence and hasNulls:
				hintSentencesCount += 1
				
			if not isFullHitSentence and hasNulls:
				print( "NOT FULL HINTS SENTENCE PATH: " + filePath )
										
			if not IsProjective( segments ):
				nonProjectiveCount += 1
				
				if hasNulls:
					nullAndNonProjectiveCount += 1
					
			if hasNulls:
				nullSentencesCount += 1
				totalWordsinNullSentencesCount += sentenceWordsCount - nullsCount
				
				partsOfSpeech.sort()
				
				partsOfSpeechUnion = ''
				for p in partsOfSpeech:
					if( len( partsOfSpeechUnion ) > 0 ):
						partsOfSpeechUnion += ','
					partsOfSpeechUnion += p
					
				if nullsCount == 1:
					addToMap( oneNullSentencesStatistics, partsOfSpeechUnion )

				if nullsCount == 2:
					addToMap( twoNullsSentencesStatistics, partsOfSpeechUnion )

			totalWordsCount += sentenceWordsCount - nullsCount
				
			maxNullCount = max( maxNullCount, nullsCount )
			
			if nullsCount > 0:
				addToMap( nullCountToSentencesCount, nullsCount )

#Iteration dir
for dir in os.listdir( rootPath ):
	if os.path.isdir( os.path.join( rootPath, dir ) ) and not( dir in blackList ):
		print( dir )
		dirsCount += 1
		logFile.write( "!!!!!!!!!!!     " + os.path.join( rootPath, dir ) + "   !!!!!!!!!!!!!!!\n" )
		oldCount = nullSentencesCount
		
		for file in os.listdir( os.path.join( rootPath, dir ) ):
			if file.endswith( ".tgt" ):
				oldCount2 = nullSentencesCount
				processTgtFile( os.path.join( rootPath, dir, file ) )
				
				if oldCount2 != nullSentencesCount:
					logFile.write( "NULL SENTENCES IN FILE: " + str( nullSentencesCount - oldCount2 ) + '\n' )
					
		if oldCount != nullSentencesCount:
			logFile.write( "######## NULL SENTENCES IN DIR: " + str( nullSentencesCount - oldCount ) + '\n' )
		logFile.write( "\n" )
		
#Output statistics
outputFile.write( "DIRS COUNT: " + str( dirsCount ) + "\n" )
outputFile.write( "FILES COUNT: " + str( filesCount ) + "\n" )
outputFile.write( "SENTENCES COUNT: " + str( sentencesCount ) + "\n" )
outputFile.write( "SENTENCES WITH NULLS COUNT: " + str( nullSentencesCount ) + "\n" )
outputFile.write( "MAX SENTENCES NULLS COUNT: " + str( maxNullCount ) + "\n" )
outputFile.write( "NULLS STATISTICS: " + str( nullCountToSentencesCount ) + "\n" )
outputFile.write( "PARTS OF SPEECH STATISTICS: " + str( partOfSpeechToNullsCount ) + "\n" )
outputFile.write( "AVG SENTENCE LENGTH: " + str( totalWordsCount * 1.0 / sentencesCount ) + "\n" )
outputFile.write( "AVG NULL SENTENCE LENGTH: " + str( totalWordsinNullSentencesCount * 1.0 / nullSentencesCount ) + "\n" )
outputFile.write( "ONE NULL SENTENCES STATISCS: " + str( oneNullSentencesStatistics ) + "\n" )
outputFile.write( "TWO NULLS SENTENCES STATISCS: " + str( twoNullsSentencesStatistics ) + "\n" )
outputFile.write( "NON PROJECTIVE SENTENCES STATISCS: " + str( nonProjectiveCount ) + "\n" )
outputFile.write( "NON PROJECTIVE WITH NULL SENTENCES STATISCS: " + str( nullAndNonProjectiveCount ) + "\n" )
outputFile.write( "SENTENCES WITH NULL-VERB-ROOT COUNT: " + str( verbRootNullSentencesCount ) + "\n" )
outputFile.write( "NULLS WITH HINTS COUNT: " + str( nullWithHintsCount ) + "\n" )
outputFile.write( "FULL HINTS SENTENCES COUNT: " + str( hintSentencesCount ) + "\n" )

#Close file
logFile.close()
outputFile.close()
