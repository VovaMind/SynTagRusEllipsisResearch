### This folder contains: ###
* nullTest.py. Tool for computation various statistics for SynTagRus corpora.
* nullEval.py. Evaluates quality of analysis which don't consider ellipsis. We evalute such analysis on null sentences and calculate recall and precision.
* nullTestExport.py. Remove null words from extracted null senteces. We do it before start analysis null sentences. 
* nullCheck.py. Calculate statistics for various null senteces:
  * All null words have non-null children.
  * All null words dont have non-null children.
  * Mix for null words (have both null words variants).
* malttabExporter.py. Export from SynTagRus format to Malt-TAB format.
* malttabEval.py. Estimate of MaltParser analysis qualtity.
* FeaturesExtractor.py. Classify features extraction.
* FeaturesExtractor2.py. Classify features extraction. Features are a bit different.
