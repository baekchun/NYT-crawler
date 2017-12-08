from readFile import *
from translate import *
from similarity import *

file_index = [55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,75,77,78,79,81,84,85,87,88,89,90,91,92,93,94,95,97,98,99]
for i in file_index:
	file_name = "output__0"+str(i)+".txt"

	#start, first read file from txt
	eng_list, chn_list = read_file(file_name)

	print(len(eng_list))
	print(len(chn_list))

	#now sentence start:
	eng_pointer = 0
	chn_pointer = 0
	threshold = 0.0279
	length_threshold = 25
	t = Translate()

	# print(eng_list[27])
	# print(chn_list[27])
	# print(chn_list[33])
	# print(symmetric_sentence_similarity(eng_list[8],t.translate(chn_list[8])))
	# print(chn_list[8].strip()+chn_list[9].strip())
	# print(symmetric_sentence_similarity(eng_list[8],t.translate(chn_list[8].strip() + ' ' + chn_list[9].strip())))
	with open('output__0'+str(i)+'_aligned.txt','wt') as f:
		while(eng_pointer < len(eng_list)):
			print(eng_pointer)
			print(chn_pointer)
			curr_eng_sentence = eng_list[eng_pointer]
			f.write(curr_eng_sentence)
			f.write('\n')
			eng_length = len(curr_eng_sentence.split(' '))
			if chn_pointer >= len(chn_list) - 1:
				f.write(chn_list[len(chn_list) - 1])
				f.write('\n')
				break
			curr_chn_sentence = chn_list[chn_pointer]
			next_chn_sentence = chn_list[chn_pointer + 1]
			curr_translation = t.translate(curr_chn_sentence)
			next_translation = t.translate(next_chn_sentence)
			curr_length = len(curr_translation.strip().split(' '))
			next_length = len(next_translation.strip().split(' '))
			if eng_pointer == 0:
				#first check the length
				if(abs(eng_length - next_length - curr_length) >= length_threshold):
					f.write(curr_chn_sentence)
					f.write('\n')
					chn_pointer = chn_pointer + 1
				else:
					#second check similarity
					first_score = symmetric_sentence_similarity(curr_eng_sentence, curr_translation)
					second_score = symmetric_sentence_similarity(curr_eng_sentence, curr_translation.strip() + ' ' + next_translation.strip())
					if(second_score - first_score > threshold and first_score > 0.29):
						f.write(curr_chn_sentence)
						f.write(next_chn_sentence)
						f.write('\n')
						chn_pointer = chn_pointer + 2
					else:
						f.write(curr_chn_sentence)
						f.write('\n')
						chn_pointer = chn_pointer + 1
			else:
				prev_chn_sentence = chn_list[chn_pointer - 1]
				#check prev, curr, next
				prev_translation = t.translate(prev_chn_sentence)
				prev_length = len(prev_translation.strip().split(' '))
				if(abs(eng_length - prev_length) < length_threshold):
					prev_score = symmetric_sentence_similarity(curr_eng_sentence, prev_translation)
				else:
					prev_score = -1
				if(abs(eng_length - curr_length) < length_threshold):
					curr_score = symmetric_sentence_similarity(curr_eng_sentence, curr_translation)
				else:
					curr_score = -1
				if(abs(eng_length - next_length) < length_threshold):
					next_score = symmetric_sentence_similarity(curr_eng_sentence, next_translation)
				else:
					next_score = -1
				print(prev_score,curr_score, next_score)
				max_score = max(prev_score,curr_score, next_score)
				if(max_score == prev_score):
					two_score = symmetric_sentence_similarity(curr_eng_sentence, prev_translation.strip()+' '+curr_translation.strip())
					if(two_score - prev_score > threshold and prev_score > 0.29):
						f.write(prev_chn_sentence)
						f.write(curr_chn_sentence)
						f.write('\n')
						chn_pointer = chn_pointer + 1
					else:
						f.write(prev_chn_sentence)
						f.write('\n')
				elif(max_score == curr_score):
					two_score = symmetric_sentence_similarity(curr_eng_sentence, curr_translation.strip()+' '+next_translation.strip())
					if(two_score - curr_score > threshold and curr_score > 0.29):
						f.write(curr_chn_sentence)
						f.write(next_chn_sentence)
						f.write('\n')
						chn_pointer = chn_pointer + 2
					else:
						f.write(curr_chn_sentence)
						f.write('\n')
						chn_pointer = chn_pointer + 1			
				elif(max_score == next_score):
					#first examine next of next exists
					if(chn_pointer == len(chn_list) - 2):
						f.write(next_chn_sentence)
						f.write('\n')
						chn_pointer = chn_pointer + 2
					else:
						next_next_chn_sentence = chn_list[chn_pointer + 2]
						next_next_translation = t.translate(next_next_chn_sentence)
						two_score = symmetric_sentence_similarity(curr_eng_sentence, next_translation.strip()+' '+next_next_translation.strip())
						if(two_score - next_score > threshold and next_score > 0.29):
							f.write(next_chn_sentence)
							f.write(next_next_chn_sentence)
							f.write('\n')
							chn_pointer = chn_pointer + 3
						else:
							f.write(next_chn_sentence)
							f.write('\n')
							chn_pointer = chn_pointer + 2

			eng_pointer = eng_pointer + 1
			print("finish one english sentence")




