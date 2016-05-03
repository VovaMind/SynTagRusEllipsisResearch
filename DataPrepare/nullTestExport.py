# запуск: nullTestExport.py исходный_экспорт_нульПредложений экспорт_нульПредложений_без_нулей
# -*- coding: utf-8 -*-

#Export to MaltTAB data format
import os
import random
import sys
from xml.dom.minidom import *

with open(sys.argv[1], 'r', encoding='utf8') as inputNullFile:
	with open(sys.argv[2], 'w', encoding='utf8') as testNullFile:
		while (True):
			s1 = inputNullFile.readline()
			if s1 == '':
				break
			
			list = s1.split('\t')
			if len(list) < 4:
				testNullFile.write(s1)
				continue
				
			if list[0] != 'NULL':
				testNullFile.write(list[0] + '\t' + list[1] + '\t' + '0' + '\t' + list[3])
