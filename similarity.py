# this code is based on the tutorial
# from the website
# nlpforhackers.io/wordnet-sentence-similarity/ 


from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn


def penn_to_wn(tag):
	if tag.startswith('N'):
		return 'n'

	if tag.startswith('V'):
		return 'v'

	if tag.startswith('J'):
		return 'a'

	if tag.startswith('R'):
		return 'r'

	return None

def tagged_to_synset(word, tag):
	wn_tag = penn_to_wn(tag)

	if wn_tag is None:
		return None

	try:
		return wn.synsets(word, wn_tag)[0]
	except:
		return None


def sentence_similarity(sentence1, sentence2):
	""" compute the sentence similarity using wordnet """

	sentence1 = pos_tag(word_tokenize(sentence1))
	sentence2 = pos_tag(word_tokenize(sentence2))

	s1 = list()
	s2 = list()


	synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
	synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

	synsets1 = [ss for ss in synsets1 if ss]
	synsets2 = [ss for ss in synsets2 if ss]

	score, count = 0.0, 0

	for syn1 in synsets1:
		arr_simi_score = []
		for syn2 in synsets2:
			simi_score = syn1.path_similarity(syn2)

			if simi_score is not None:
				arr_simi_score.append(simi_score)

			if(len(arr_simi_score) > 0):
				best = max(arr_simi_score)
				score += best
				count += 1

	# Average the values
	if count == 0:
		return 0
	else:
		score /= count
		return score

def symmetric_sentence_similarity(sentence1, sentence2):
	return (sentence_similarity(sentence1, sentence2) + sentence_similarity(sentence2, sentence1)) / 2



