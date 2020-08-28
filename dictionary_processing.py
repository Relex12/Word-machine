"""
## This module allows you to **manage** input and output files and to **process** the dictionary.
"""

####################################
# Input and output file management #
####################################

def open_alphabet (filename="alphabet.txt"):
    """
    `open_alphabet()` gets the input alphabet from a file.

    * **filename** (*str*) : the name of the file to open (`read` mode)
    * **return** (*list*) : the input alphabet
    """
    f = open(filename, "r")
    alphabet = f.read().split(' ')
    f.close()
    while '\n' in alphabet:
        alphabet.remove('\n')
    alphabet.insert(0, '')
    return alphabet

def open_dictionary(filename="dictionary.txt"):
    """
    `open_dictionary()` gets the input dictionary from a file.

    * **filename** (*str*) : the name of the file to open (`read` mode)
    * **return** (*list*) : the input dictionary
    """
    f = open(filename, "r")
    dictionary = f.read().split('\n')
    f.close()
    while '' in dictionary:
        dictionary.remove('')
    return dictionary

def get_alphabet_from_dict(dictionary):
    """
    `get_alphabet_from_dict()` gets the alphabet from the dictionary by adding each used letter.

    * **dictionary** (*list*) : the input dictionary (before processing)
    * **return** (*list*) : the alphabet based on the letters used in the dictionary
    """
    alphabet = []
    for word in dictionary:
        for letter in word:
            if not letter in alphabet:
                alphabet.append(letter)

    alphabet = list(sorted(set(alphabet)))
    alphabet.insert(0, '')
    return alphabet

def write_clean_dictionary(dictionary, filename="output_dictionary.txt"):
    """
    `write_clean_dictionary()` writes the processed dictionary in a file.

    * **dictionary** (*list*) : the input dictionary (after processing)
    * **filename** (*str*) : the name of the file to open (`write` mode)
    * **return** (*None*)
    """
    f = open(filename, 'w')
    for word in dictionary:
        f.write(word+'\n')
    f.close()

def write_generated_words(word_list, filename="generated_words.txt"):
    """
    `write_generated_words()` writes the list of generated words in a file.

    * **word_list** (*str*) : the string that contain all generated words
    * **filename** (*str*) : the name of the file to open (`write` mode)
    * **return** (*None*)
    """
    f = open(filename, 'w')
    f.write(word_list)
    f.close()

#########################
# Dictionary processing #
#########################

def process_dictionary (dictionary):
    """
    `process_dictionary()` sorts the dictionary and removes duplicated words.

    * **dictionary** (*list*) : the input dictionary (while processing)
    * **return** (*list*) : the sorted dictionary without duplicated words
    """
    return sorted(set(dictionary))

def remove_missing_letters(dictionary, missing_letters):
    """
    `get_missing_letters()` removes from the dictionary every word that uses at least one letter that is not in the alphabet.

    * **dictionary** (*list*) : the input dictionary (while processing)
    * **missing_letters** (*list*) : letters used in the dictionary that are not in the alphabet
    * **return** (*list*) : the dictionary without any word that contain one word from **missing_letters**
    """
    words_to_del = []
    for letter in missing_letters:
        for word in dictionary:
            if letter in word:
                words_to_del.append(word)
    words_to_del = set(words_to_del)
    for word in words_to_del:
        dictionary.remove(word)
    return dictionary

def get_missing_letters (dictionary, alphabet):
    """
    `get_missing_letters()` gets every word from the dictionary that uses at least one letter that is not in the alphabet.

    * **dictionary** (*list*) : the input dictionary (while processing)
    * **alphabet** (*list*) : the used alphabet (from input file or from dictionary)
    * **return** (*list*) : the list of letters used at least once in the dictionary that are not in the alphabet
    """
    missing_letter = []
    for word in dictionary:
        for letter in word:
            if not letter in alphabet and not letter in missing_letter:
                missing_letter.append(letter)
    return (missing_letter)

def print_plural_words (dictionary, lang):
    """
    `print_plural_words()` prints every word from the dictionary that is already in the dictionary in singular form.

    * **dictionary** (*list*) : the input dictionary (while processing)
    * **lang** (*str*) : the language used to follow plural rules (only `FR` is available yet)
    * **return** (*None*)
    """
    if lang == 'fr':
        for word in dictionary:
            l = len(word)
            if word[l-1] == 's'and word[:l-1] in dictionary \
            or word[l-1] == 'x'and word[:l-1] in dictionary \
            or l > 3 and word[l-3:l] == 'aux'and word[:l-3]+'al' in dictionary \
            or l > 3 and word[l-3:l] == 'aux'and word[:l-3]+'ail' in dictionary:
                print(word)
    # insert here plural rules from other languages

def remove_plural_words (dictionary, lang):
    """
    `remove_plural_words()` removes from the dictionary every word that is already in the dictionary in singular form.

    * **dictionary** (*list*) : the input dictionary (while processing)
    * **lang** (*str*) : the language used to follow plural rules (only `FR` is available yet)
    * **return** (*list*) : the dictionary without duplicated words in singular / plural forms
    """
    words_to_del = []
    if lang == 'fr':
        for word in dictionary:
            l = len(word)
            if word[l-1] == 's'and word[:l-1] in dictionary \
            or word[l-1] == 'x'and word[:l-1] in dictionary \
            or l > 3 and word[l-3:l] == 'aux'and word[:l-3]+'al' in dictionary \
            or l > 3 and word[l-3:l] == 'aux'and word[:l-3]+'ail' in dictionary:
                words_to_del.append(word)
    words_to_del = set(words_to_del)
    for word in words_to_del:
        dictionary.remove(word)
    # HERE insert plural rules from other languages
    return (dictionary)

def lower_case_words(dictionary):
    """
    `lower_case_words()` lower-cases every word from the dictionary.

    * **dictionary** (*list*) : the input dictionary (while processing)
    * **return** (*list*) : the dictionary with each word lower-cased
    """
    return ([word.lower() for word in dictionary])

def print_acronyms (dictionary):
    """
    `print_acronyms()` prints every acronyms from the dictionary.
    An acronyms is a word such as `word == word.upper()`.

    * **dictionary** (*list*) : the input dictionary (while processing)
    * **return** (*None*)
    """
    for word in dictionary:
        if word == word.upper():
            print(word)

def remove_acronyms (dictionary):
    """
    `remove_acronyms()` removes every acronyms from the dictionary.
    An acronyms is a word such as `word == word.upper()`.

    * **dictionary** (*list*) : the input dictionary (while processing)
    * **return** (*list*) : the dictionary without acronyms
    """
    words_to_del = []
    for word in dictionary:
        if word == word.upper():
            words_to_del.append(word)
    words_to_del = set(words_to_del)
    for word in words_to_del:
        dictionary.remove(word)
    return (dictionary)
