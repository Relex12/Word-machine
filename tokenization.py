#!/usr/bin/env python3

"""
## This module allows you to **tokenize** dictionaries for better results.
"""

from anagram import *
from dictionary import *
from generation import *

# Workaround for matplotlib import freeze on WSL2 Win11
import os
os.environ["DISPLAY"] = ":0"

import matplotlib.pyplot as plt
import numpy as np


def check_tokenizable(dictionary):
	"""`check_tokenizable()` checks if the dictionary contains any word with a digit or an uppercase character.

	* **dictionary** (*list*): the input dictionary (after processing)
	* **return** (*bool*) False if any digit or uppercase character, True otherwise
	"""
	for word in dictionary:
		if any(char.isupper() or char.isdigit() for char in word):
			return False
	return True

def find_max(matrix, alphabet):
	""" `find_max()` finds the most frequent character sequence.

    * **matrix** (*dict*): the matrix representing the probability of letter chaining each other
    * **alphabet** (*list*): the used alphabet (from input file or from dictionary)
    * **return** (*tuple*): the most frequent consecutive character sequence
	"""
	max = 0
	i = j = ''
	for el1 in alphabet:
		for el2 in alphabet:
			if matrix[el1][el2] > max:
				max = matrix[el1][el2]
				i, j = el1, el2
	return (i, j)

def build_2D_substitute_matrix(dictionary, alphabet, substitute_dict):
    """`build_2D_substitute_matrix()` initiate and fill a 2 dimension matrix (dict of dict object) by browsing the dictionary.

    * **dictionary** (*list*): the input dictionary (after processing)
    * **alphabet** (*list*): the used alphabet (from input file or from dictionary)
	* **substitute_dict** (*dict*): the substituted characters indexed by single substitution character
    * **return** (*dict*): the matrix representing the probability of letter chaining each other
	"""
    # initiate the matrix
    matrix = dict()
    substitute_alphabet = alphabet+list(substitute_dict.keys())
    for i in substitute_alphabet:
        matrix[i] = dict()
        for l in substitute_alphabet:
            matrix[i][l] = 0

    # fill matrix with dictionary
    for word in dictionary:
        for substitute, original_letters in substitute_dict.items():
            word = word.replace(original_letters, substitute)
        previous_letter = word[0]
        for current_letter in word[1:]:
            matrix[previous_letter][current_letter]+=1
            previous_letter = current_letter
    return matrix

def print_2D_matrix(matrix, alphabet):
	"""`print_2D_matrix()` print the matrix row by row.s

    * **matrix** (*dict*): the matrix representing the probability of letter chaining each other
    * **alphabet** (*list*): the used alphabet (from input file or from dictionary)
	* **return** (*None*)
	"""
	print (alphabet)
	for line in matrix:
		print (line, matrix[line])

def plot_2D_matrix(matrix, alphabet, filename):
	"""`plot_2D_matrix()` plot the matrix in a diagram using matplotlib.

    * **matrix** (*dict*): the matrix representing the probability of letter chaining each other
    * **alphabet** (*list*): the used alphabet (from input file or from dictionary)
    * **filename** (*str*): the name of the file to plot in
	* **return** (*None*)
	"""
	l = len(alphabet)
	X, Y = np.meshgrid(np.linspace(0, l-1, l), np.linspace(0, l-1, l))
	Z = []

	i = 0
	for el1 in alphabet:
		Z.append([])
		for el2 in alphabet:
			Z[i].append(matrix[el1][el2])
		i+=1

	fig, ax = plt.subplots()
	ax.imshow(Z)
	ax.set_xticks(range(len(alphabet)))
	ax.set_xticklabels(alphabet)
	ax.set_yticks(range(len(alphabet)))
	ax.set_yticklabels(alphabet)
	plt.savefig(filename)

def write_substitute_dictionary(dictionary, substitute_dict, filename):
    """`write_substitute_dictionary()` writes the dictionary in a file with substitutions.

    * **dictionary** (*list*): the input dictionary (after processing)
	* **substitute_dict** (*dict*): the substituted characters indexed by single substitution character
    * **filename** (*str*): the name of the file to open (`write` mode)
    * **return** (*None*)
    """
    f = open(filename, 'w')
    for word in dictionary:
        for substitute, original_letters in substitute_dict.items():
            word = word.replace(original_letters, substitute)
        f.write(word+'\n')
    f.close()


def substitution(word, substitute_dict):
	"""`substitution()` encode a word from human readable to substitute.

    * **word** (*str*): the word to encode
	* **substitute_dict** (*dict*): the substituted characters indexed by single substitution character
	* **return** (*str*): the encoded word
	"""
	substituted_items = substitute_dict.items()
	substituted_values = substitute_dict.values()
	while(any(encoded in word for encoded in substituted_values)):
		copy = word
		for substitute, encoded in substituted_items:
			if encoded in copy:
				copy = copy.replace(encoded, substitute)
		word = copy
	return word



def reverse_substitution(word, substitute_dict):
	"""`reverse_substitution()` decode a word from substitute to human readable.

    * **word** (*str*): the word to decode back
	* **substitute_dict** (*dict*): the substituted characters indexed by single substitution character
	* **return** (*str*): the decoded word
	"""
	while(any(char.isupper() or char.isdigit() for char in word)):
		copy = word
		for char in word:
			if char in substitute_dict:
				copy = copy.replace(char, substitute_dict[char])
		word = copy
	return word

# TODO: use dynamic UTF-8 characters as substitutes instead of a static list of characters
substitute_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
substitute_dict = dict()
