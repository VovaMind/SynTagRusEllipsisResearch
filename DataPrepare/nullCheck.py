import os
import sys

nullWithChild = 0
nullWithoutChild = 0
sentences = {"allWith" : 0, "allWithout" : 0, "both" : 0}

def processSentence(prevs, isNulls):
	global nullWithChild
	global nullWithoutChild
	
	wordsWithParents = set()
	for prev, isNull in zip(prevs, isNulls):
		if not isNull:
			wordsWithParents.add(int(prev))
		
	for index, isNull in zip(range(1, len(prevs) + 1), isNulls):
		if isNull:
			if index in wordsWithParents:
				nullWithChild += 1
			else:
				nullWithoutChild += 1

outputf = open(sys.argv[2], 'w', encoding='utf8')
with open(sys.argv[1], 'r', encoding='utf8') as nullFile:
	isOver = False
	prevs = []
	isNulls = []
	old = [0, 0]
	sentenceStrs = []
	
	while True:
		str2 = nullFile.readline()
		if str2 == '':
			isOver = True
		else:
			sentenceStrs.append(str2)
		parts = str2.split('\t')
		if (len(parts) < 4):
			processSentence(prevs, isNulls)

			if nullWithChild == old[0]:
				sentences['allWithout'] += 1
			elif nullWithoutChild == old[1]:
				sentences['allWith'] += 1
			else:
				sentences['both'] += 1
			
			if nullWithoutChild == old[1]:
				for s in sentenceStrs:
					outputf.write(s)
				outputf.write('\n')
			prevs = []
			isNulls = []
			sentenceStrs = []
			
			old = [nullWithChild, nullWithoutChild]
		else:
			prevs.append(parts[2])
			isNulls.append(parts[0] == 'NULL')
			
		if isOver:
			break

print("Nulls with child count: " + str(nullWithChild))
print("Nulls without child count: " + str(nullWithoutChild))
print("Sentences: " + str(sentences))
