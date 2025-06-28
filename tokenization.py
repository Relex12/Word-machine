#!/usr/bin/env python3

"""TODO"""

from anagram import *
from dictionary import *
from generation import *

# export DISPLAY=:0
import matplotlib.pyplot as plt
import numpy as np


# TODO: rework into find_n_max
def find_max(matrix):
	max = 0
	i = j = ''
	for el1 in alphabet:
		for el2 in alphabet:
			if matrix[el1][el2] > max:
				max = matrix[el1][el2]
				i, j = el1, el2
	return (i, j)

def build_2D_substitute_matrix(dictionary, alphabet):
    # initiate the matrix
    matrix = dict()
    for i in alphabet:
        matrix[i] = dict()
        for l in alphabet:
            matrix[i][l] = 0

    # fill matrix with dictionary
    for word in dictionary:
        previous_letter = word[0]
        for current_letter in word[1:]:
            matrix[previous_letter][current_letter]+=1
            previous_letter = current_letter
    return matrix

def print_2D_matrix(matrix, alphabet):
	print (alphabet)
	for line in matrix:
		print (line, matrix[line])

def plot_2D_matrix(matrix, alphabet, filename):
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

def write_substitute_dictionary(dictionary, first, second, substitute, filename):
    """
    `write_substitute_dictionary()` writes the processed dictionary in a file. TODO

    * **dictionary** (*list*): the input dictionary (after processing)
	* TODO
	* TODO
	* TODO
    * **filename** (*str*): the name of the file to open (`write` mode)
    * **return** (*None*)
    """
    f = open(filename, 'w')
    for word in dictionary:
        f.write(word.replace(first+second, substitute)+'\n')
    f.close()


def reverse_substitution(word, substitute_dict):
	while(any(char.isupper() or char.isdigit() for char in word)):
		copy = word
		for char in word:
			if char in substitute_dict:
				copy = copy.replace(char, substitute_dict[char])
		word = copy
	return word

# TODO: do not use a static list of substitute characters but dynamic UTF-8 characters that are not in initial dictionary
substitute_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
substitute_dict = dict()


dictionary = lower_case_words(process_dictionary(open_dictionaries(["../Dictionaries/last-name-fr.txt"])))

(min_len, max_len) = get_length_range(dictionary, 85)

# TODO: use a dynamic number of substitutions, so must find a way to determine when to stop
for substitute in substitute_list:
	alphabet = get_alphabet_from_dict(dictionary)

	if '' in alphabet:
		alphabet.remove('')
	alphabet.append(find_separator(alphabet))

	matrix = build_2D_substitute_matrix(dictionary, alphabet)

	# plot_2D_matrix(matrix, alphabet, f"out/image-{substitute}.png")

	i, j = find_max(matrix)

	# TODO: stop substituting one by one, substitute as long as there is no collision with substitutions from the same wave
	# TODO: write every substitution in the same file again and again, named after original dictionaries, minimize space usage
	write_substitute_dictionary(dictionary, i, j, substitute, f"out/dict-{substitute}.txt")

	dictionary = process_dictionary(open_dictionaries([f"out/dict-{substitute}.txt"]))

	# TODO: use progress bar
	print (f"replacing {i}{j} with {substitute}")

	substitute_dict[substitute] = i+j

alphabet = get_alphabet_from_dict(dictionary)

if '' in alphabet:
	alphabet.remove('')
alphabet.append(find_separator(alphabet))

matrix = build_ND_matrix(dictionary, alphabet, 4)


word_list = []
# word generation
failed_attempts = 0
error = None
nb_word_to_gen = 30
while len(word_list) != nb_word_to_gen:
	word = reverse_substitution(generate_word_ND(matrix, alphabet, '', 4), substitute_dict)
	# check word compliancy
	if len(word) < min_len or max_len < len(word):
		failed_attempts += 1
		if failed_attempts >= 50:
			error = 'size not compliant'
	# elif args.new and word in dictionary:
	# 	failed_attempts += 1
	# 	if failed_attempts >= args.max_attempts:
	# 		error = 'word already in dictionary'
	# elif word in word_list:
	# 	failed_attempts += 1
	# 	if failed_attempts >= args.max_attempts:
	# 		error = 'word already generated'
	else:
		word_list.append(word)
		failed_attempts = 0

	if error is not None:
		raise Exception(f"maximum number of attempts exceeded: generation failed {50} times in a raw, maybe increase this value with --max-attempts, last failure due to {error}")

for word in word_list:
	print (word)
