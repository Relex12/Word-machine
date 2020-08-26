import sys

from word_machine import *
from dictionary_processing import *

##################################
# Command line option processing #
##################################

class MissingArgumentError(Exception):
    def __init__(self, option):
        self.option = option

def get_option_value(option, mandatory):
    """
        gets the value of the specified option from the command-line interface

        :param str option: the specified option
        :param boolean mandatory: an error is being raised if true and the option has no value
        :return: the value of the specified option
        :rtype: string
    """
    position = sys.argv.index(option) + 1
    if len(sys.argv) == position or sys.argv[position][0] == '-':
        if mandatory:
            # print ('# WARNING: Missing argument for {} option, execution will fail'.format(option))
            raise MissingArgumentError (option)
                # the function exits properly, then a TypeError stops the run
                # it should stop in this function instead of exiting it
    else:
        return sys.argv[position]

#############################
# Main zone : executed code #
#############################

if __name__ == '__main__':

    arg_list = ['-alpha', '-dict', '-write', '-gen', '-force', '-low-case', \
                '-size', '-no-acronyms', '-output', '-prefix', '-no-plural', \
                '-new','-print-acronyms', '-print-plural', '-dim', '-capitalize']

    for arg in sys.argv:
        if arg[0] == '-' and not arg in arg_list:
            print ("Error: unrecognized argument", arg)

    # getting dictionary
    if '-dict' in sys.argv:
        dictionary = open_dictionary(get_option_value('-dict', True))
    else:
        dictionary = open_dictionary()

    dictionary = process_dictionary(dictionary)

    if '-print-acronyms' in sys.argv:
        print_acronyms (dictionary)

    if '-print-plural' in sys.argv:
        print_plural_words (dictionary, get_option_value('-print-plural', True))

    if '-no-acronyms' in sys.argv:
        dictionary = remove_acronyms(dictionary)

    if '-low-case' in sys.argv:
        dictionary = lower_case_words(dictionary)

    if '-no-plural' in sys.argv:
        dictionary = remove_plural_words(dictionary, get_option_value('-no-plural', True))

    # getting alphabet
    if '-alpha' in sys.argv:
        alphabet = open_alphabet(get_option_value ('-alpha', True))
        missing_letters = get_missing_letters(dictionary, alphabet)
        if '-force' in sys.argv:
            dictionary = remove_unknown_letters (dictionary, missing_letters)
        else:
            if missing_letters != []:
                print ('WARNING: Some characters are used in the dictionary without being in the alphabet')
                print (missing_letters)
    else:
        alphabet = get_alphabet_from_dict (dictionary)



    if '-write' in sys.argv:
        filename = get_option_value('-write', False)
        if filename == None:
            write_clean_dictionary (dictionary)
        else:
            write_clean_dictionary (dictionary, filename)

    # if '-plot' in sys.argv:
        # matrix_2D = initiate_empty_2D_matrix(alphabet)
        # build_2D_matrix (matrix_2D, dictionary)
        # plot_2D_matrix(matrix_2D, alphabet)

    if '-gen' in sys.argv:

        if '-dim' in sys.argv and get_option_value('-dim', True) == '2':
            matrix = initiate_empty_2D_matrix(alphabet)
            build_2D_matrix(matrix, dictionary)
        else:
            matrix = initiate_empty_3D_matrix(alphabet)
            build_3D_matrix(matrix, dictionary)

        output_file = '-output' in sys.argv
        word_list = ""

        prefix = '-prefix' in sys.argv
        if prefix:
            prefix = get_option_value('-prefix', True)

        required_size = '-size' in sys.argv
        if required_size:
            required_size = int(get_option_value('-size', True))

        new_only = '-new' in sys.argv

        i = 0
        while i != int(get_option_value('-gen', True)):
            if '-dim' in sys.argv and get_option_value('-dim', True) == '2':
                word = generate_word_2D(matrix, alphabet, prefix)
            else:
                word = generate_word_3D(matrix, alphabet, prefix)
            if '-capitalize' in sys.argv:
                word = word.capitalize()
            if (required_size == False or len(word) == required_size) \
            and not (new_only and word in dictionary):
                if output_file:
                    word_list += word + '\n'
                else:
                    print (word)
                i-=-1

        if output_file:
            filename = get_option_value('-output', False)
            if filename == None:
                write_generated_words(word_list)
            else:
                write_generated_words(word_list, filename)
