rem %1 - parsing model (malt parser config file). we got it from learning. if %1 = 'test' we get test.mco
rem %2 - data file
java -jar C:\SyntUp\maltparser-1.8\maltparser-1.8.jar -c %1 -i %2 -m learn -if malttab
