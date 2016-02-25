
def find_common_distinct_letters (word1, word2):
	letters_word1 = []
	letters_word2 = []
	
	for i in range(0,len(word1)):
		letters_word1.append(word1[i])
	for i in range(0,len(word2)):
		letters_word2.append(word2[i])
	common_distinct_letters = list(set(letters_word1).union(set(letters_word2)))
	return len(common_distinct_letters)


print find_common_distinct_letters('cat','bat')