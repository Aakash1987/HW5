#Unit tests for spellChecker.py

#Import everything from the file with functions to be tested
from spellChecker import *
#Use this line in every unit testing file
import unittest



class spellChecker(unittest.TestCase):
	#self is a keyword, can't change
	#def setUp(self):

	def test_ignoreCaseAndPunc(self):
		#Tests the case with an upper case and ',' in input
		self.assertEqual('actually', ignoreCaseAndPunc('Actually,'), 'print lsterror message')
		#Tests the case with upper case and '.' in input
		self.assertEqual('variables', ignoreCaseAndPunc('variABles.'), 'print lsterror message')
		#Tests the case with hyphen - Should not be changed
		self.assertEqual('co-exist', ignoreCaseAndPunc('co-exist'), 'print lsterror message')

	def test_findWordInDictionary(self):
		#Tests a couple of words in the dictionary after removing punctuations
		self.assertEqual(True, findWordInDictionary('Ada,','TestDict'), 'print lsterror message')
		self.assertEqual(True, findWordInDictionary("Afghanistan!!",'TestDict'), 'print lsterror message')
		#Tests a word not in dictionary
		self.assertEqual(False, findWordInDictionary('Adultss?','TestDict'), 'print lsterror message')

	def test_getWordsOfSimLength(self):
		#Tests both n-1 and n+1 type of similar length words
		self.assertEqual(set(['ACM','a','Ada']), set(getWordsOfSimLength('Ab', 'TestDict', 1)), 'print lsterror message')

	def test_getWordsWithSameStart(self):
		#Tests the same word for different number of first common letters
		self.assertEqual(set(['afgh','afghan','afghanistansd']), set(getWordsWithSameStart('Afghan', ['Afg,','Afgh?','!Afghan','Afghanistansd'], 4)), 'print lsterror message')
		self.assertEqual(set(['afg','afgh','afghan','afghanistansd']), set(getWordsWithSameStart('Afghan', ['Afg,','Afgh?','!Afghan','Afghanistansd'], 3)), 'print lsterror message')
	
	def test_getWordsWithCommonLetters(self):
		test_list = ['ban', 'bang', 'gang', 'aa', 'mange']
		#Tests a case with no repeated letters in the test word
		self.assertEqual(set(['gang','bang','mange']), set(getWordsWithCommonLetters('clang', test_list, 3)), 'print lsterror message')
		#Tests a case with repeated letters in the test word
		self.assertEqual(set(['mange']), set(getWordsWithCommonLetters('immediate', test_list, 3)), 'print lsterror message')

	def test_getSimilarityMetric(self):
		#Tests simple cases
		self.assertEqual(2.5, getSimilarityMetric('oblige', 'oblivion'), 'print lsterror message')
		self.assertEqual(1.5, getSimilarityMetric('aghast!', 'gross?'), 'print lsterror message')

	def test_getSimilarityDict(self):
		#Tests simple cases
		wordList = ['ban', 'bang', 'gang', 'aa', 'mange']
		function_output = getSimilarityDict('band', wordList)
		expected_output = {'ban': 1.5, 'bang': 3, 'gang': 2, 'aa': 0.5, 'mange': 1.0}
		self.assertEqual(function_output, expected_output, 'print lsterror message')

	def test_sortIn2D(self):
		#Tests simple cases
		expected_output = [['Steven', 24], ['Ben', 25], ['arv', 33], ['fed', 45]]
		data = [['arv', 33], ['fed', 45], ['Ben', 25], ['Steven', 24]]
		data.sort(sortIn2D)
		self.assertEqual(data,expected_output,'print lsterror message')

	def test_getListOfFirstComponents(self):
		#Tests simple cases
		self.assertEqual([1,3], getListOfFirstComponents([(1,2), (3,4)]), 'print lsterror message')

	def test_getBestWords(self):
		#Tests simple cases
		similarityDictionary = {'ban': 1.5, 'bang': 3, 'gang': 2, 'aa': 0.5, 'mange': 1.0}
		self.assertEqual(['bang','gang','ban'], getBestWords(similarityDictionary, 3), 'print lsterror message')

	def test_find_total_distinct_letters(self):
		#Tests simple cases
		self.assertEqual((4,2), find_total_distinct_letters('cat','bat'), 'print lsterror message')
		self.assertEqual((4,3), find_total_distinct_letters('pull','paul'), 'print lsterror message')

	def test_getWordSuggestionsV1(self):
		#Tests the +/- n length rule
		expected_output = ['africa', 'african', 'alaska', 'alden', 'ascii', 'albania', "ada's", "atm's", 'alabama']
		function_output = getWordSuggestionsV1('Africn', 'TestDict', 1, 0, 10)
		self.assertEqual(expected_output, function_output, 'print lsterror message')
		#Tests the common percent rule by checking the top suggestion provided
		expected_output = ['african']
		function_output = getWordSuggestionsV1('Africn', 'TestDict', 1, 100, 10)
		self.assertEqual(expected_output, function_output, 'print lsterror message')
		expected_output = ['africa', 'african']
		function_output = getWordSuggestionsV1('Africn', 'TestDict', 1, 75, 10)
		self.assertEqual(expected_output, function_output, 'print lsterror message')
		
		

	def test_getWordSuggestionsV2(self):
		#Tests the +/- 1 letter rule
		expected_output = ['africa', 'african', 'alaska', 'alden', 'ascii', 'albania', "ada's", "atm's", 'alabama']
		function_output = getWordSuggestionsV2('africn','TestDict',0,10)
		self.assertEqual(expected_output, function_output, 'print lsterror message')

		#Tests the common start and common end functionality
		expected_output = ['raxxxxce','rxxxxxxe']
		function_output = getWordSuggestionsV2('rayyyyce','TestDict',1,10)
		self.assertEqual(expected_output, function_output, 'print lsterror message')

		#Tests the common start and common end functionality
		expected_output = ['raxxxxce']
		function_output = getWordSuggestionsV2('rayyyyce','TestDict',2,10)
		self.assertEqual(expected_output, function_output, 'print lsterror message')

	def test_getCombinedWordSuggestions(self):
		#Input that satisfies v1 but not v2
		expected_output = ['raxxxxce']
		function_output = getCombinedWordSuggestions('raxxce', 'TestDict')
		self.assertEqual(expected_output, function_output, 'print lsterror message')
		
		#Input that satisfies both v1 and v2
		expected_output = ['raxxxxce','rxxxxxxe']
		function_output = getCombinedWordSuggestions('raxxxxce', 'TestDict')
		self.assertEqual(expected_output, function_output, 'print lsterror message')
		
		
		

unittest.main()














