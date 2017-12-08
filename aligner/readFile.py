import re
from pyltp import SentenceSplitter
def read_file(file_name):
	english_list = list()
	chinese_list = list()
	#read part

	changeFlag = 0
	with open(file_name, 'rt') as f:
		for line in f:
			if '*' in line:
				changeFlag = 1
				continue
			if changeFlag == 0:
				#separate the english paragraph
				sentenceEnders = re.compile(r"""
				# Split sentences on whitespace between them.
				(?:               # Group for two positive lookbehinds.
				  (?<=[.!?])      # Either an end of sentence punct,
				| (?<=[.!?]['"])  # or end of sentence punct and quote.
				)                 # End group of two positive lookbehinds.
				(?<!  Mr\.   )    # Don't end sentence on "Mr."
				(?<!  Mrs\.  )    # Don't end sentence on "Mrs."
				(?<!  Jr\.   )    # Don't end sentence on "Jr."
				(?<!  Dr\.   )    # Don't end sentence on "Dr."
				(?<!  Prof\. )    # Don't end sentence on "Prof."
				(?<!  Sr\.   )    # Don't end sentence on "Sr."
				(?<!  A\.    )
				(?<!  B\.    )
				(?<!  C\.    )
				(?<!  D\.    )
				(?<!  E\.    )
				(?<!  F\.    )
				(?<!  G\.    )
				(?<!  H\.    )
				(?<!  I\.    )
				(?<!  J\.    )
				(?<!  K\.    )
				(?<!  L\.    )
				(?<!  M\.    )
				(?<!  N\.    )
				(?<!  O\.    )
				(?<!  P\.    )
				(?<!  Q\.    )
				(?<!  R\.    )
				(?<!  S\.    )
				(?<!  T\.    )
				(?<!  U\.    )
				(?<!  V\.    )
				(?<!  W\.    )
				(?<!  X\.    )
				(?<!  Y\.    )
				(?<!  Z\.    )
				(?<!  Oct\.    )
				(?<!  Dec\.    )
				(?<!  Rep\.    )
				(?<!  Sept\.    )
				\s+               # Split on whitespace between sentences.
				""", 
				re.VERBOSE)
				sentenceList = sentenceEnders.split(line.strip())
				english_list.extend(sentenceList)
			if changeFlag == 1:
				sents = SentenceSplitter.split(line.strip())
				chinese_list.extend(sents)			

	return english_list, chinese_list