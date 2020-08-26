import sys

from word_machine import *
from dictionary_processing import *

##################################
# Command line option processing #
##################################

class MissingArgumentError(Exception):
    def __init__(self, option):
        self.option = option

class UnrecognizedArgumentError(Exception):
    def __init__(self, arg):
        self.arg = arg

class SizeValueError(Exception):
    def __init__(self, value):
        self.option = value

def get_option_value(option, shorter=None, mandatory=True):
    """
        gets the value of the specified option from the command-line interface

        :param str option: the specified option
        :param boolean mandatory: an error is being raised if true and the option has no value
        :return: the value of the specified option
        :rtype: string
    """
    if option in sys.argv:
        position = sys.argv.index(option) + 1
    # elif:
    #     print ("SAUCISSE")
    else:
        position = sys.argv.index(shorter) + 1
    if len(sys.argv) == position or sys.argv[position][0] == '--':
        if mandatory:
            raise MissingArgumentError (option)
    else:
        return sys.argv[position]

arg_list = ['--help', '--version', '-d', '--dict','--alpha', '--write',\
            '--output', '--force', '--low-case', '--print-acronyms', \
            '--print-plural', '--no-acronyms', '--no-plural', '-g',  '--generate', \
            '--dim', '--capitalize', '-s', '--size', '--prefix', '--new']

#############################
# Main zone : executed code #
#############################

if __name__ == '__main__':

    for arg in sys.argv:
        if arg[0] == '-' and not arg in arg_list:
            raise UnrecognizedArgumentError (arg)

    if '--help' in sys.argv:
        f = open("description.txt", "r")
        print (f.read())
        f.close()
    elif '--version' in sys.argv:
        f = open("version.txt", "r")
        print (f.read())
        f.close()
    else:
        # getting dictionary
        if '--dict' in sys.argv or '-d' in sys.argv:
            dictionary = open_dictionary(get_option_value('--dict', shorter='-d'))
        else:
            dictionary = open_dictionary()

        dictionary = process_dictionary(dictionary)

        if '--print-acronyms' in sys.argv:
            print_acronyms (dictionary)

        if '--print-plural' in sys.argv:
            print_plural_words (dictionary, get_option_value('--print-plural'))

        if '--no-acronyms' in sys.argv:
            dictionary = remove_acronyms(dictionary)

        if '--low-case' in sys.argv:
            dictionary = lower_case_words(dictionary)

        if '--no-plural' in sys.argv:
            dictionary = remove_plural_words(dictionary, get_option_value('--no-plural'))

        # getting alphabet
        if '--alpha' in sys.argv:
            alphabet = open_alphabet(get_option_value ('--alpha'))
            missing_letters = get_missing_letters(dictionary, alphabet)
            if '--force' in sys.argv:
                dictionary = remove_unknown_letters (dictionary, missing_letters)
            else:
                if missing_letters != []:
                    print ('WARNING: Some characters are used in the dictionary without being in the alphabet')
                    print (missing_letters)
        else:
            alphabet = get_alphabet_from_dict (dictionary)



        if '--write' in sys.argv:
            filename = get_option_value('--write', mandatory=False)
            if filename == None:
                write_clean_dictionary (dictionary)
            else:
                write_clean_dictionary (dictionary, filename)

        # if '--plot' in sys.argv:
            # matrix_2D = initiate_empty_2D_matrix(alphabet)
            # build_2D_matrix (matrix_2D, dictionary)
            # plot_2D_matrix(matrix_2D, alphabet)

        if '--generate' in sys.argv or '-g' in sys.argv :

            if '--dim' in sys.argv and get_option_value('--dim') == '2':
                matrix = build_2D_matrix(dictionary, alphabet)
            else:
                matrix = build_3D_matrix(dictionary, alphabet)


            output_file = '--output' in sys.argv
            word_list = ""

            prefix = '--prefix' in sys.argv
            if prefix:
                prefix = get_option_value('--prefix')

            size_option = '--size' in sys.argv or '-s' in sys.argv
            min_len = 0
            max_len = sys.maxsize
            if size_option:
                size_option = get_option_value('--size', shorter='-s')
                if ':' == size_option:
                    raise SizeValueError (size_option)
                elif not ':' in size_option:
                    min_len = max(int(size_option), min_len)
                    max_len = min(int(size_option), max_len)
                elif size_option.startswith(':'):
                    max_len = int(size_option[1:])
                elif size_option.endswith(':'):
                    min_len = int(size_option[:-1])
                else:
                    min_len = max(int(size_option.split(':')[0]), min_len)
                    max_len = min(int(size_option.split(':')[-1]), max_len)
                if max_len < min_len:
                    raise SizeValueError (size_option)

            new_only = '--new' in sys.argv

            i = 0
            number_of_words = int(get_option_value('--generate', shorter='-g'))
            while i != number_of_words:
                if '--dim' in sys.argv and get_option_value('--dim') == '2':
                    word = generate_word_2D(matrix, alphabet, prefix)
                else:
                    word = generate_word_3D(matrix, alphabet, prefix)
                if '--capitalize' in sys.argv:
                    word = word.capitalize()
                if (min_len <= len(word) and len(word) <= max_len) \
                and not (new_only and word in dictionary):
                        if output_file:
                            word_list += word + '\n'
                        else:
                            print (word)
                        i-=-1

            if output_file:
                filename = get_option_value('--output', mandatory=False)
                if filename == None:
                    write_generated_words(word_list)
                else:
                    write_generated_words(word_list, filename)
