"""
## This module allows you to **build** the matrix from the processed dictionary and **generate** words.
"""

from random import choices
from itertools import product

###########################################
# N dimensions matrix, N-1 letters before #
###########################################

def build_ND_matrix(dictionary, alphabet, N):
    """
    `build_ND_matrix()` initiate and fill a N dimension matrix (dict of dict object) by browsing the dictionary.

    * **dictionary** (*list*): the input dictionary (after processing)
    * **alphabet** (*list*): the used alphabet (from input file or from dictionary)
    * **N** (*int*): the dimension of the matrix
    * **return** (*dict*): the matrix representing the probability of letter chaining each other
    """
    separator = alphabet[-1]

    # initiate the matrix
    matrix = dict()
    for i in product(alphabet, repeat=N-1):
        index = ''.join(i)
        matrix[index] = dict()
        for l in alphabet:
            matrix[index][l] = 0

    # fill matrix with dictionary
    for word in dictionary:
        previous_letters = (N-1)*separator
        for current_letter in word:
            matrix[previous_letters][current_letter]+=1
            previous_letters = previous_letters[1:] + current_letter
        for i in range (1,N):
            matrix[previous_letters][separator]+=1
            previous_letters = previous_letters[1:] + separator
    return matrix

def generate_word_ND(matrix, alphabet, prefix, N):
    """
    `generate_word_ND()` generates a word used the `random.choices()` method uppon the ND matrix in the last letter column.

    * **matrix** (*dict*): the matrix representing the probability of letter chaining each other
    * **alphabet** (*list*): the used alphabet (from input file or from dictionary)
    * **prefix** (*str*): the prefix requested for the generated words
    * **N** (*int*): the dimension of the matrix
    * **return** (*str*): the generated word (length variable)
    """
    separator = alphabet[-1]

    previous_letters = (N-1)*separator
    if len(prefix) < N:
        previous_letters = previous_letters[len(prefix):] + prefix
    else:
        previous_letters = prefix[len(prefix)-N+1:]

    word = prefix
    new_letter = None
    while new_letter != separator:
        new_letter = choices(population=alphabet, weights=matrix[previous_letters].values(), k=1)[0]
        # TODO: add a try catch
        # error example: ./word-machine.py -d pokemon-fr.txt -g 10 -tcn -p arti KeyError: '0M'
        # issue related to usage of prefix with token, just decode the key and throw an error asking to reduce or change the prefix
        if new_letter != separator:
            word = word+new_letter
            previous_letters = previous_letters[1:] + new_letter
    return (word)
