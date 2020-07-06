from random import choices
import sys

##################################
# Command line option processing #
##################################

class MissingArgumentError(BaseException):
    """docstring for MissingArgumentError."""

    def __init__(self, opt):
        self.opt = opt
        self.text = "Missing argument for "

def get_option(option, mandatory):
    position = sys.argv.index(option) + 1
    if len(sys.argv) == position or sys.argv[position][0] == '-':
        if mandatory:
            try:
                raise MissingArgumentError (option)
                # the function exits properly, then a TypeError stops the run
                # it should stop in this function instead of exiting it
            except MissingArgumentError as e:
                print ("Error : Missing argument for {0} option".format(option))
        return None
    else:
        return sys.argv[position]

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

###############################################
# 2 dimensions matrix, only one letter before #
###############################################

def initiate_empty_2D_matrix(alphabet):
    matrix = dict()
    for letter in alphabet:
        matrix[letter] = dict()
        for other_letter in alphabet:
            matrix[letter][other_letter] = 0
    return matrix

def build_2D_matrix(matrix, dictionary):
    for word in dictionary:
        previous_letter = ''
        for current_letter in word:
            matrix[previous_letter][current_letter] += 1
            previous_letter = current_letter
        matrix[word[len(word)-1]][''] +=1

def plot_2D_matrix(matrix, alphabet):
    print (alphabet)
    for line in matrix:
        print (line, matrix[line])
        print ('')

def generate_word_2D(matrix, alphabet):
    word = ''
    previous_letter = ''
    new_letter = None
    while new_letter != '':
        new_letter = choices(population=alphabet, weights=matrix[previous_letter].values(), k=1)[0]
        word = word+new_letter
        previous_letter = new_letter
    return (word)

###########################################
# 3 dimensions matrix, two letters before #
###########################################

def initiate_empty_3D_matrix(alphabet):
    matrix = dict()
    for letter1 in alphabet:
        matrix[letter1] = dict()
        for letter2 in alphabet:
            matrix[letter1][letter2] = dict()
            for letter3 in alphabet:
                matrix[letter1][letter2][letter3] = 0
    return matrix

def build_3D_matrix(matrix, dictionary):
    for word in dictionary:
        previous_letter1 = ''
        previous_letter2 = ''
        for current_letter in word:
            matrix[previous_letter1][previous_letter2][current_letter] += 1
            previous_letter1 = previous_letter2
            previous_letter2 = current_letter
        matrix[word[len(word)-2]][word[len(word)-1]][''] +=1
        matrix[word[len(word)-1]][''][''] +=1

def generate_word_3D(matrix, alphabet, prefix):
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

def generate_3D_from_end(matrix, alphabet, suffix):
    if len(suffix) == 1:
        next_letter1 = suffix[0]
        next_letter2 = ''
    else:
        next_letter1 = suffix[0]
        next_letter2 = suffix[1]
    word = suffix
    new_letter = None
    while new_letter != '':
        new_letter = choices(population=alphabet, weights=matrix[next_letter1][next_letter2].values(), k=1)[0]
        print (new_letter, word)
        word = new_letter+word
        next_letter1 = new_letter
        next_letter2 = next_letter1
    return (word)

#############################
# Main zone : executed code #
#############################

if __name__ == '__main__':

    arg_list = ['-alpha', '-dict', '-write', '-gen', '-force', '-low-case', \
                '-size', '-no-acronyms', '-output', '-prefix', '-no-plural', \
                '-new','-print-acronyms', '-print-plural']

    for arg in sys.argv:
        if arg[0] == '-' and not arg in arg_list:
            print ("Error: unrecognized argument", arg)

    # getting alphabet
    if '-alpha' in sys.argv:
        alphabet = open_alphabet(get_option ('-alpha', True))
    else:
        alphabet = open_alphabet()

    # getting dictionary
    if '-dict' in sys.argv:
        dictionary = open_dictionary(get_option('-dict', True))
    else:
        dictionary = open_dictionary()

    dictionary = process_dictionary(dictionary)

    if '-print-acronyms' in sys.argv:
        print_acronyms (dictionary)

    if '-print-plural' in sys.argv:
        print_plural_words (dictionary, get_option('-print-plural', True))

    if '-no-acronyms' in sys.argv:
        dictionary = remove_acronyms(dictionary)

    if '-low-case' in sys.argv:
        dictionary = lower_case_words(dictionary)

    if '-no-plural' in sys.argv:
        dictionary = remove_plural_words(dictionary, get_option('-no-plural', True))

    missing_letters = get_missing_letters(dictionary, alphabet)
    if '-force' in sys.argv:
        dictionary = remove_unknown_letters (dictionary, missing_letters)
    else:
        if missing_letters != []:
            print ('WARNING: Some characters are used in the dictionary without being in the alphabet')
            print (missing_letters)

    if '-write' in sys.argv:
        filename = get_option('-write', False)
        if filename == None:
            write_clean_dictionary (dictionary)
        else:
            write_clean_dictionary (dictionary, filename)

    # if '-plot' in sys.argv:
        # matrix_2D = initiate_empty_2D_matrix(alphabet)
        # build_2D_matrix (matrix_2D, dictionary)
        # plot_2D_matrix(matrix_2D, alphabet)

    if '-gen' in sys.argv:
        matrix_3D = initiate_empty_3D_matrix(alphabet)
        build_3D_matrix(matrix_3D, dictionary)

        output_file = '-output' in sys.argv
        word_list = ""

        prefix = '-prefix' in sys.argv
        if prefix:
            prefix = get_option('-prefix', True)

        required_size = '-size' in sys.argv
        if required_size:
            required_size = int(get_option('-size', True))

        new_only = '-new' in sys.argv

        i = 0
        while i != int(get_option('-gen', True)):
            word = generate_word_3D(matrix_3D, alphabet, prefix)
            if (required_size == False or len(word) == required_size) \
            and not (new_only and word in dictionary):
                if output_file:
                    word_list += word + '\n'
                else:
                    print (word)
                i-=-1

        if output_file:
            filename = get_option('-output', False)
            if filename == None:
                write_generated_words(word_list)
            else:
                write_generated_words(word_list, filename)
