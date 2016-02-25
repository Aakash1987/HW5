#Replacement out of range
import math

def main():
	fileName = raw_input("Please enter the name of your text file for spell checking, without the file extension. \n")

	#Opening file to read as f and file to write as mod_f
	fileName1 = fileName + '.txt'
	f = open(fileName1)
	modified_file_name = fileName + '-chk.txt'
	mod_f = open(modified_file_name,'w')

	#Initializing variables
	modified_line = []
	choice = ''
	mod_line = ''
	dict_choice = 2

	while dict_choice > 1:
		dict_choice = input("Please enter '1' to use your dictionary file for spell checking, or '0' for default dictionary. \n")
	
	if dict_choice == 0:
		dict_name = 'engDictionary'
	elif dict_choice == 1:
		dict_name = raw_input("Please enter the name of your dictionary file for spell checking, without the file extension. \n")
	
	#The program reads words in one line at a time, corrects them, writes them and then moves to the next line
	words_in_line = []
	for line in f:
		#Deal with files with multiple newline characters
		if len(line) != 0:
			line = line.split()
			for i in range(0,len(line)):
				#If the word is in the dictionary, add it to a list and move to next word
				if findWordInDictionary(line[i],dict_name):
					modified_line.append(line[i])
				
				#If word is not in dictionary, give the user three choices to correct it.

				#Case when no suggestions are found
				elif getCombinedWordSuggestions(line[i], dict_name) == []:
					print "The word",line[i], "is misspelled.\nThere are 0 suggestions in our dictionary for this word"
					choice = raw_input("Press 'a' for accept as is, 't' for type in manually.")
					#Replace the word with a new word provided by user
					while choice not in ['a','t']:
						choice = raw_input("Press 'a' for accept as is, 't' for type in manually.\n")
					if choice == 't':
						new_word = raw_input("Please type the word that will be used as the replacement in the output file \n")
						modified_line.append(new_word)
					#Leave the word as it is
					if choice == 'a':
						modified_line.append(line[i])

				#Case when you find suggestions for the word
				else:
					print "The word",line[i],"is misspelled \n", "The following suggestions are available"
					prettyPrint(getCombinedWordSuggestions(line[i], dict_name))
					#Dealing with bad user input
					while choice not in ['r','a','t']:
						choice = raw_input("Press 'r' for replace, 'a' for accept as is, 't' for type in manually.\n")
					#Replace the word with dictionary suggestions
					if choice == 'r':
						print "Your word will now be replaced with one of the suggestions." 
						choice_of_word = 100
						choice_of_word = input("Enter the number corresponding to the word that you want to use for replacement.\n")

						modified_line.append(getCombinedWordSuggestions(line[i],dict_name)[choice_of_word-1])
					#Replace the word with a new word provided by user
					if choice == 't':
						new_word = raw_input("Please type the word that will be used as the replacement in the output file \n")
						modified_line.append(new_word)
					#Leave the word as it is
					if choice == 'a':
						modified_line.append(line[i])
				
				choice = ''
		#Convert the list to string to write in new file
		for word in modified_line:
			mod_line = mod_line + word + ' '

		mod_f.write(mod_line)
		modified_line = []
		mod_line = ''

	f.close()
	mod_f.close()


def ignoreCaseAndPunc(word):
	'''Given a word that might have upper and lower case letters and punctuation, returns a word that is entirely in lower case and all punctuation removed'''
	punctuations = [',',';',':','.','!','?','\n',' ']
	for punctuation in punctuations:
		word = word.strip(punctuation)
	word = word.lower()
	return word

def findWordInDictionary(word, fileName):
	'''Check if the word is present in the file named fileName'''
	word = ignoreCaseAndPunc(word)
	fileName = fileName + '.txt'
	f = open(fileName)
	for line in f:
		line = ignoreCaseAndPunc(line)
		line = line.split()[0]
		if line == word:
			return 1
	return 0
	f.close()

def getWordsOfSimLength(word, fileName, n):
	'''Given a word, returns a list of words from the fileName that all have the length +/- a value n'''
	simLengthWords =[]
	target_length = len(word)
	fileName = fileName + '.txt'
	f = open(fileName)
	for line in f:
		#line = ignoreCaseAndPunc(line)
		line = line.split()[0]
		length = len(line)
		if length <= (target_length+n) and length >= (target_length-n):
			simLengthWords.append(line)
	return simLengthWords
	f.close()

def getWordsWithSameStart(word, wordList, n):
	'''Given a word and a list of words, returns a list of words that have at least the first n characters the same'''
	same_start =[]
	word = ignoreCaseAndPunc(word)
	for words_in_list in wordList:
		words_in_list = ignoreCaseAndPunc(words_in_list)
		if word[:n] == words_in_list[:n]:
			same_start.append(words_in_list)
	return same_start

def getWordsWithCommonLetters(word, wordList, n):
	'''Given a word, returns a list of words that have n or more letters in common'''
	common_words =[]
	letters_in_word =[]
	counter = 0
	word = ignoreCaseAndPunc(word)
	for letters in word:
		letters_in_word.append(letters)
	unique_letters = set(letters_in_word)

	for words_in_list in wordList:
		words_in_list = ignoreCaseAndPunc(words_in_list)
		for letters in unique_letters:
			if letters in words_in_list:
				counter = counter + 1
		if counter >= n:
			common_words.append(words_in_list)
		counter = 0
	return common_words

def getSimilarityMetric(word1, word2):
	''' Given two words, this function computes two measures of similarity and returns the average'''
	counter = 0
	word1 = ignoreCaseAndPunc(word1)
	word2 = ignoreCaseAndPunc(word2)
	common_length = min(len(word1),len(word2))
	for i in range(0,common_length):
		if word1[i] == word2[i]:
			counter = counter + 1
	leftSimilarity = counter

	counter = 0
	for i in range(1,common_length+1):
		if word1[-i] == word2[-i]:
			counter = counter + 1
	rightSimilarity = counter

	avg_similarity = (leftSimilarity+rightSimilarity)/2.0
	return avg_similarity

def getSimilarityDict(word, wordList):
	'''Creates a dictionary with words in wordList as keys and the average similarity as the values.'''
	similarity_dict = {}
	for word_in_list in wordList:
		similarity_dict[word_in_list] = getSimilarityMetric(word_in_list,word)
	return similarity_dict

def sortIn2D(tup1,tup2):
	'''Sorts two tuples with two components, based on the second component'''
	if tup1[-1] < tup2[-1]: 
		return -1
	elif tup1[-1] == tup2[-1]: 
		return 0
	return 1

def getListOfFirstComponents(tupleList):
	'''Takes in a list of tuples and returns another list which has just the first components of the tuples'''
	first_components = []
	for tuples in tupleList:
		component = tuples[0]
		first_components.append(component)
	return first_components

def getBestWords(similarityDictionary, n):
	'''Takes a Dictionary, sorts it and returns the top n keys in terms of the value.'''
	listOfTuples = similarityDictionary.items()
	listOfTuples.sort(sortIn2D, reverse=True)
	return getListOfFirstComponents(listOfTuples)[0:n]

def getWordSuggestionsV1(word, fileName, n, commonPercent, topN):
	'''Given a word, return a list of topN suggestions from fileName based on an algorithm'''
	shortlisted_words = []
	word = ignoreCaseAndPunc(word)

	#Condition1 - Get words within +/- n length
	sim_length_words = getWordsOfSimLength(word, fileName, n)

	for word_new in sim_length_words:
		word_new = ignoreCaseAndPunc(word_new)
		total_distinct_letters = find_total_distinct_letters (word_new, word)[0]
		common_distinct_letters = find_total_distinct_letters (word_new, word)[1]
		required_common = math.ceil(float(total_distinct_letters) * float(commonPercent) / 100)
		# Condition 2 - Takes only words which have more than commonPercent letters in common
		if required_common <= common_distinct_letters:
			shortlisted_words.append(word_new)

	Similarity_Dict = getSimilarityDict(word, shortlisted_words)
	top_suggestions = getBestWords(Similarity_Dict, topN)
	return top_suggestions

def getWordSuggestionsV2(word, fileName, n, topN):
	'''Given a word, return a list of topN suggestions from fileName based on an algorithm'''
	reversed_similar_start_words = []	
	wordSuggestions = []

	close_length_words = getWordsOfSimLength(word, fileName, 1)
	similar_start_words = getWordsWithSameStart(word, close_length_words, n)
	
	for words in similar_start_words:
		#Reverses a string
		words = words[::-1]
		reversed_similar_start_words.append(words)	

	reverse_word = word[::-1]
	similar_end_words = getWordsWithSameStart(reverse_word,reversed_similar_start_words,n)

	for words in similar_end_words:
		#Reverses a string
		words = words[::-1]
		wordSuggestions.append(words)

	Similarity_Dict = getSimilarityDict(word, wordSuggestions)
	top_suggestions = getBestWords(Similarity_Dict, topN)
	return top_suggestions

def getCombinedWordSuggestions(word, fileName):
	'''Combines the list of suggestions provided by getWordSuggestionsV1 and getWordSuggestionsV2 based on an algorithm'''
	v1_suggestions = getWordSuggestionsV1(word, fileName, 2, 75, 7)
	v2_suggestions = getWordSuggestionsV2(word, fileName, 1, 7)
	suggestions = list(set(v1_suggestions).union(set(v2_suggestions)))
	Similarity_Dict = getSimilarityDict(word, suggestions)
	top_suggestions = getBestWords(Similarity_Dict, 10)
	return top_suggestions

def prettyPrint(lst):
	'''Prints a list in a numbered format'''
	for i in range(0,len(lst)):
		print str(i+1) + '. ' + lst[i]

def find_total_distinct_letters (word1, word2):
	'''Finds common distinct letters and total distinct letters between two words'''
	letters_word1 = []
	letters_word2 = []
	
	for i in range(0,len(word1)):
		letters_word1.append(word1[i])
	for i in range(0,len(word2)):
		letters_word2.append(word2[i])
	total_distinct_letters = list(set(letters_word1).union(set(letters_word2)))
	common_distinct_letters = list(set(letters_word1).intersection(set(letters_word2)))
	return (len(total_distinct_letters),len(common_distinct_letters))

def autocorrect (fileName, dictionary):
	'''Chooses the top suggestion from the spell check and rewrites the file'''

	fileName1 = fileName + '.txt'
	f = open(fileName1)
	modified_file_name = fileName + '-chk.txt'
	mod_f = open(modified_file_name,'w')

	#Initializing variables
	modified_line = []
	mod_line = ''
	dict_name = dictionary
	#The program reads words in one line at a time, corrects them, writes them and then moves to the next line
	words_in_line = []
	for line in f:
		#Deal with files with multiple newline characters
		if len(line) != 0:
			line = line.split()
			for i in range(0,len(line)):
				#If the word is in the dictionary, add it to a list and move to next word
				if findWordInDictionary(line[i],dict_name):
					modified_line.append(line[i])
				#If word not in dictionary, but no suggestions, keep it as is.
				elif getCombinedWordSuggestions(line[i], dict_name) == []:
					modified_line.append(line[i])
				#If word not in dictionary, and there are suggestions, use the top suggestion
				else:
					modified_line.append(getCombinedWordSuggestions(line[i],dict_name)[0])
		#Convert the list to string to write in new file
		for word in modified_line:
			mod_line = mod_line + word + ' '

		mod_f.write(mod_line)
		mod_f.write('\n')
		modified_line = []
		mod_line = ''

	f.close()
	mod_f.close()


if __name__ == '__main__':
    main()