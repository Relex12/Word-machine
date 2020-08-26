####################################
# Input and output file management #
####################################

def open_alphabet (filename="alphabet.txt"):
    f = open(filename, "r")
    alphabet = f.read().split(' ')
    f.close()
    while '\n' in alphabet:
        alphabet.remove('\n')
    alphabet.insert(0, '')
    return alphabet

def open_dictionary(filename="dictionary.txt"):
    f = open(filename, "r")
    dictionary = f.read().split('\n')
    f.close()
    while '' in dictionary:
        dictionary.remove('')
    return dictionary

def get_alphabet_from_dict(dictionary):
    alphabet = []
    for word in dictionary:
        for letter in word:
            if not letter in alphabet:
                alphabet.append(letter)

    alphabet.insert(0, '')
    return list(sorted(set(alphabet)))

def write_clean_dictionary(dictionary, filename="output_dictionary.txt"):
    f = open(filename, 'w')
    for word in dictionary:
        f.write(word+'\n')
    f.close()

def write_generated_words(word_list, filename="generated_words.txt"):
    f = open(filename, 'w')
    f.write(word_list)
    f.close()

#########################
# Dictionary processing #
#########################

def process_dictionary (dictionary):
    return sorted(set(dictionary))

def remove_unknown_letters(dictionary, missing_letters):
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
    missing_letter = []
    for word in dictionary:
        for letter in word:
            if not letter in alphabet and not letter in missing_letter:
                missing_letter.append(letter)
    return (missing_letter)

def print_plural_words (dictionary, lang):
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
    # insert here plural rules from other languages
    return (dictionary)

def lower_case_words(dictionary):
    return ([word.lower() for word in dictionary])

def print_acronyms (dictionary):
    for word in dictionary:
        if word == word.upper():
            print(word)

def remove_acronyms (dictionary):
    words_to_del = []
    for word in dictionary:
        if word == word.upper():
            words_to_del.append(word)
    words_to_del = set(words_to_del)
    for word in words_to_del:
        dictionary.remove(word)
    return (dictionary)
