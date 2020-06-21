from random import choices

def open_alphabet (filename):
    f = open(filename, "r")
    alphabet = f.read().split(' ')
    f.close()
    while '\n' in alphabet:
        alphabet.remove('\n')
    alphabet.insert(0, '')
    return alphabet

def open_dictionary(filename):
    f = open(filename, "r")
    dictionary = f.read().split('\n')
    f.close()
    while '' in dictionary:
        dictionary.remove('')
    return dictionary

def test_dictionary (dictionary, alphabet):
    dictionary = sorted(set(dictionary))
    plural_words = []
    missing_letter = []
    for word in dictionary:
        if word[len(word)-1] == 's':
            if word[:len(word)-1] in dictionary:
                plural_words.append(word)
        for letter in word:
            if not letter in alphabet and not letter in missing_letter:
                missing_letter.append(letter)
    print (plural_words)
    print (missing_letter)
    # problème : renvoi d'objets vides
    return (dictionary, plural_words, missing_letter)

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

def generate_word_2D(matrix, alphabet):
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

if __name__ == '__main__':

    alphabet = open_alphabet ("alphabet2.txt")
    dictionary = open_dictionary("légendaires-copie")

#    print (test_dictionary(dictionary, alphabet)[1:2])

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

    matrix_3D = initiate_empty_3D_matrix(alphabet)

    build_3D_matrix(matrix_3D, dictionary)

    for i in range(1, 100):
        print (generate_word_2D(matrix_3D, alphabet))
