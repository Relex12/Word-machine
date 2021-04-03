"""
## This module allows you to **build** the matrix from the processed dictionary and to **generate** words.
"""

from random import choices

###############################################
# 2 dimensions matrix, only one letter before #
###############################################

def build_2D_matrix(dictionary, alphabet):
    """
    `build_2D_matrix()` initiate and fill a 2D matrix (dict of dict object) by browsing the dictionary.

    * **dictionary** (*list*) : the input dictionary (after processing)
    * **alphabet** (*list*) : the used alphabet (from input file or from dictionary)
    * **return** (*dict*) : the matrix representing the probability of letter chaining each other
    """
    # initiate matrix
    matrix = dict()
    for letter in alphabet:
        matrix[letter] = dict()
        for other_letter in alphabet:
            matrix[letter][other_letter] = 0

    # fill matrix with dictionary
    for word in dictionary:
        previous_letter = ''
        for current_letter in word:
            matrix[previous_letter][current_letter] += 1
            previous_letter = current_letter
        matrix[word[len(word)-1]][''] +=1
    return matrix

# def plot_2D_matrix(matrix, alphabet):
#     print (alphabet)
#     for line in matrix:
#         print (line, matrix[line])
#         print ('')

def generate_word_2D(matrix, alphabet, prefix):
    """
    `generate_word_3D()` generates a word used the `random.choices()` method uppon the 3D matrix in the last letter column.

    * **matrix** (*dict*) : the matrix representing the probability of letter chaining each other
    * **alphabet** (*list*) : the used alphabet (from input file or from dictionary)
    * **prefix** (*str*) : the prefix requested for the generated words
    * **return** (*str*) : the generated word (length variable)
    """
    if prefix == False:
        word = ''
        previous_letter = ''
    else:
        word = prefix
        previous_letter = prefix[-1]
    new_letter = None
    while new_letter != '':
        new_letter = choices(population=alphabet, weights=matrix[previous_letter].values(), k=1)[0]
        word = word+new_letter
        previous_letter = new_letter
    return (word)

###########################################
# 3 dimensions matrix, two letters before #
###########################################

def build_3D_matrix(dictionary, alphabet):
    """
    `build_3D_matrix()` initiate and fill a 3D matrix (dict of dict of dict object) by browsing the dictionary.

    * **dictionary** (*list*) : the input dictionary (after processing)
    * **alphabet** (*list*) : the used alphabet (from input file or from dictionary)
    * **return** (*dict*) : the matrix representing the probability of letter chaining each other
    """
    # initiate matrix
    matrix = dict()
    for letter1 in alphabet:
        matrix[letter1] = dict()
        for letter2 in alphabet:
            matrix[letter1][letter2] = dict()
            for letter3 in alphabet:
                matrix[letter1][letter2][letter3] = 0

    # fill matrix with dictionary
    for word in dictionary:
        previous_letter1 = ''
        previous_letter2 = ''
        for current_letter in word:
            matrix[previous_letter1][previous_letter2][current_letter] += 1
            previous_letter1 = previous_letter2
            previous_letter2 = current_letter
        matrix[word[len(word)-2]][word[len(word)-1]][''] +=1
        matrix[word[len(word)-1]][''][''] +=1
    return matrix

def generate_word_3D(matrix, alphabet, prefix):
    """
    `generate_word_3D()` generates a word used the `random.choices()` method uppon the 3D matrix in the last letter column.

    * **matrix** (*dict*) : the matrix representing the probability of letter chaining each other
    * **alphabet** (*list*) : the used alphabet (from input file or from dictionary)
    * **prefix** (*str*) : the prefix requested for the generated words
    * **return** (*str*) : the generated word (length variable)
    """
    if prefix == False:
        word = ''
        previous_letter1 = ''
        previous_letter2 = ''
    elif len(prefix) == 1:
        word = prefix
        previous_letter1 = ''
        previous_letter2 = prefix[-1]
    else:
        word = prefix
        previous_letter1 = prefix[-2]
        previous_letter2 = prefix[-1]
    new_letter = None
    while new_letter != '':
        new_letter = choices(population=alphabet, weights=matrix[previous_letter1][previous_letter2].values(), k=1)[0]
        word = word+new_letter
        previous_letter1 = previous_letter2
        previous_letter2 = new_letter
    return (word)
