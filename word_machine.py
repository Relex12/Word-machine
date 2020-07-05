from random import choices
import sys

##################################
# Command line option processing #
##################################

def get_option(option):
    position = sys.argv.index(option)
    if len(sys.argv) == position or sys.argv[position+1][0] == '-':
        # raise the error instead of printing it
        print ("Error : Missing argument for '"+option+"' option")
    # no else need if raised
    else:
        return sys.argv[position+1]

####################################
# Input and output file management #
####################################

def open_alphabet (filename="alphabet.txt"):
    # attention au \n si il n'y a pas d'espace final
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
    for i in range(1, 10):
        for letter in missing_letters:
            for word in dictionary:
                if letter in word:
                    # print (letter, word)
                    dictionary.remove(word)
                    # print (word in dictionary)
    return dictionary

def get_missing_letters (dictionary, alphabet):
    missing_letter = []
    for word in dictionary:
        for letter in word:
            if not letter in alphabet and not letter in missing_letter:
                missing_letter.append(letter)
    return (missing_letter)

def remove_plural_words (dictionary):
    # incomplete
    for word in dictionary:
        if word[len(word)-1] == 's':
            if word[:len(word)-1] in dictionary:
                dictionary.remove(word)
    return (dictionary)

def get_plural_words (dictionary):
    # incomplete
    plural_words = []
    for word in dictionary:
        if word[len(word)-1] == 's':
            if word[:len(word)-1] in dictionary:
                plural_words.append(word)
    return (plural_words)

def lower_case_words(dictionary):
    return ([word.lower() for word in dictionary])

def remove_acronyms (dictionary):
    for i in range (1, 4):
        for word in dictionary:
            if word == word.upper():
                print (word)
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

def generate_word_3D(matrix, alphabet):
    word = ''
    previous_letter1 = ''
    previous_letter2 = ''
    new_letter = None
    while new_letter != '':
        new_letter = choices(population=alphabet, weights=matrix[previous_letter1][previous_letter2].values(), k=1)[0]
        word = word+new_letter
        previous_letter1 = previous_letter2
        previous_letter2 = new_letter
    return (word)


#############################
# Main zone : executed code #
#############################

if __name__ == '__main__':

    # getting alphabet
    if '-a' in sys.argv:
        alphabet = open_alphabet(get_option ('-a'))
    else:
        alphabet = open_alphabet()

    # getting dictionary
    if '-d' in sys.argv:
        dictionary = open_dictionary(get_option('-d'))
    else:
        dictionary = open_dictionary()

    dictionary = process_dictionary(dictionary)

    if '-ac' in sys.argv:
        dictionary = remove_acronyms(dictionary)

    if '-lc' in sys.argv:
        dictionary = lower_case_words(dictionary)

    missing_letters = get_missing_letters(dictionary, alphabet)
    if '-r' in sys.argv:
        dictionary = remove_unknown_letters (dictionary, missing_letters)
    else:
        if missing_letters != []:
            print ('WARNING: Some characters are used in the dictionary without being in the alphabet')
            print (missing_letters)

    if '-w' in sys.argv:
        write_clean_dictionary (dictionary)


###############################################
# 2 dimensions matrix, only one letter before #
###############################################

    # matrix_2D = initiate_empty_2D_matrix(alphabet)
    # build_2D_matrix (matrix_2D, dictionary)
    # plot_2D_matrix(matrix_2D, alphabet)
    # for i in range(1, 10):
    #     print (generate_word_2D(matrix_2D, alphabet))

###########################################
# 3 dimensions matrix, two letters before #
###########################################

    if '-g' in sys.argv:
        matrix_3D = initiate_empty_3D_matrix(alphabet)
        build_3D_matrix(matrix_3D, dictionary)

        output_file = '-o' in sys.argv
        word_list = ""

        if '-s' in sys.argv:
            required_size = int(get_option('-s'))
            i = 0
            while i != int(get_option('-g')):
                word = generate_word_3D(matrix_3D, alphabet)
                if len(word) == required_size:
                    if output_file:
                        word_list += word + '\n'
                    else:
                        print (word)
                    i-=-1

        else:
            for i in range(1, int(get_option('-g'))):
                word = generate_word_3D(matrix_3D, alphabet)
                if output_file:
                    word_list += word + '\n'
                else:
                    print (word)

        if output_file:
            write_generated_words(word_list, get_option('-o'))
