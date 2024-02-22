#!/usr/bin/env python3

"""
## This module allows you to **execute** the code and manages command-line options.
"""

import argparse
from sys import maxsize

from generation import *
from dictionary import *

class SizeValueError(Exception):
    """
    a `SizeValueError` is raised when the argument given to the `--size` option is not one of the followings : `NUM`, `:NUM`, `NUM:` or `NUM:NUM`.
    * **value** is the argument that did not match any possible value of the `--size` option
    """
    def __init__(self, value):
        self.value = value

class MaxAttemptsExceededError(Exception):
    """
    a `MaxAttemptsExceededError` is raised when the generation of a new word failed more times than the maximum number of attempts, based on the given generation rules.
    * **value** is the maximum number of attempts
    """
    def __init__(self, value):
        self.value = value

#############################
# Main zone : executed code #
#############################

if __name__ == '__main__':

########################
# Arguments processing #
########################

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version", action="version", version='1.0')
    parser.add_argument("-d", "--dict", metavar='FILE', nargs='*', help="specify the dictionary files")
    parser.add_argument("-a", "--alpha", metavar='FILE', type=str, help="specify the alphabet file (alphabet is deduced from the dictionary if not specified)")
    parser.add_argument("-w", "--write", metavar='FILE', type=str, help="write the processed dictionary in the specified file")
    parser.add_argument("-o", "--output", metavar='FILE', type=str, help="write generated words in the specified file")
    parser.add_argument("--nb-columns", metavar='NUM', type=int, default=1, help="specify the number of columns tu use to display the generated words")
    parser.add_argument("-f", "--force", action='store_true', help="remove from the dictionary every word with at least one letter not in the alphabet (ignored if --alpha is absent)")
    parser.add_argument("--low-case", action='store_true', help="lowercase every word from the dictionary")
    parser.add_argument("--print-acronyms", action='store_true', help="print acronyms from the dictionary to stdout")
    parser.add_argument("--print-plural", metavar='LANG', type=str, help="print to sdout the plural words whose singular is in the dictionary (depends on the language only FR is available yet)")
    parser.add_argument("--no-acronyms", action='store_true', help="remove acronyms from the dictionary")
    parser.add_argument("--no-plural", metavar='LANG', type=str, help="remove plural words from the dictionary")
    parser.add_argument("-g", "--gen", metavar='NUM', type=int, help="generate as many words as specified (option required for every option below)")
    parser.add_argument("--dim", metavar='NUM', type=int, choices=range(2,3+1), default=3, help="use the specified dimension for the matrix (between 2 and 3)")
    parser.add_argument("-c", "--capitalize", action='store_true', help="capitalize generated words")
    parser.add_argument("-s", "--size", help="specify the length of generated words. SIZE can be NUM (equals) NUM: (less than) :NUM (more than) NUM:NUM (between)")
    parser.add_argument("-p", "--prefix", type=str, help="specify a prefix for all generated words")
    parser.add_argument("-n", "--new", action='store_true', help="generate words that are not in the dictionary and not already generated")
    parser.add_argument("--max_attempts", metavar='NUM', type=int, default=50, help="specify the number of tries to generate a new word before throwing an error")

    args = parser.parse_args()


    # getting dictionary
    dictionary = process_dictionary(open_dictionaries(args.dict))

    if args.print_acronyms:
        print_acronyms (dictionary)

    if args.print_plural is not None:
        print_plural_words (dictionary, args.print_plural)

    if args.no_acronyms:
        dictionary = remove_acronyms(dictionary)

    if args.low_case:
        dictionary = lower_case_words(dictionary)

    if args.no_plural is not None:
        dictionary = remove_plural_words(dictionary, args.no_plural)

    # getting alphabet
    if args.alpha is not None:
        alphabet = open_alphabet(args.alpha)
        missing_letters = get_missing_letters(dictionary, alphabet)
        if args.force:
            dictionary = remove_missing_letters (dictionary, missing_letters)
        else:
            if missing_letters != []:
                print ('WARNING: Some characters are used in the dictionary without being in the alphabet')
                print (missing_letters)
    else:
        alphabet = get_alphabet_from_dict (dictionary)



    if args.write is not None:
        filename = args.write
        write_clean_dictionary (dictionary, filename)

    # if '--plot' in sys.argv:
        # matrix_2D = initiate_empty_2D_matrix(alphabet)
        # build_2D_matrix (matrix_2D, dictionary)
        # plot_2D_matrix(matrix_2D, alphabet)

    if args.gen is not None:

        if args.dim == 2:
            matrix = build_2D_matrix(dictionary, alphabet)
        else:
            matrix = build_3D_matrix(dictionary, alphabet)


        output_file = args.output is not None
        word_list = []

        prefix = args.prefix is not None
        if prefix:
            prefix = args.prefix


        size_option = args.size is not None
        min_len = 0
        max_len = maxsize
        if size_option:
            size_option = args.size
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

        nb_word_added = 0
        failed_attempts = 0
        number_of_words = args.gen
        while nb_word_added != number_of_words:
            if args.dim == 2:
                word = generate_word_2D(matrix, alphabet, prefix)
            else:
                word = generate_word_3D(matrix, alphabet, prefix)
            if args.capitalize:
                word = word.capitalize()
            if (min_len <= len(word) and len(word) <= max_len) \
            and (not args.new or args.new and not word in dictionary) \
            and not word in word_list :
                word_list.append(word)
                nb_word_added += 1
                failed_attempts = 0
            else:
                failed_attempts += 1
                if failed_attempts >= args.max_attempts:
                    raise MaxAttemptsExceededError (args.max_attempts)


        column_word_list = [[]]

        for word in word_list:
            if len(column_word_list[-1]) == args.nb_columns:
                column_word_list.append([])
            column_word_list[-1].append(word)

        while len(column_word_list[-1]) != args.nb_columns:
            column_word_list[-1].append(" ")

        col_widths = [max(map(len, col)) for col in zip(*column_word_list)]
        output_words = ""
        for row in column_word_list:
            output_words += "  ".join((val.ljust(width) for val, width in zip(row, col_widths))) + '\n'

        if output_file:
            filename = args.output
            write_generated_words(output_words, filename)
        else:
            print (output_words)
