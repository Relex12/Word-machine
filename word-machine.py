#!/usr/bin/env python3

"""
## This module allows you to **execute** the code and manages command-line options.
"""

import argparse
from sys import maxsize

from generation import *
from dictionary import *


#############################
# Main zone : executed code #
#############################

if __name__ == '__main__':

########################
# Arguments processing #
########################

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--dict", metavar='FILE', nargs='*', help="specify the dictionary files")
    parser.add_argument("-g", "--gen", metavar='NUM', type=int, help="generate as many words as specified (option required for every option below)")
    parser.add_argument("--dim", metavar='NUM', type=int, choices=range(2,6), default=3, help="use the specified dimension for the matrix (between 2 and 3)")
    parser.add_argument("-n", "--new", action='store_true', help="generate words that are not in the dictionary and not already generated")
    parser.add_argument("-p", "--prefix", type=str, default='', help="specify a prefix for all generated words")
    parser.add_argument("-c", "--capitalize", action='store_true', help="capitalize generated words")
    parser.add_argument("-s", "--size", help="specify the length of generated words. SIZE can be 'NUM' (equals) 'NUM:' (less than) ':NUM' (more than) 'NUM:NUM' (between) or ':' (any)")
    parser.add_argument("-a", "--average-size", metavar='PER', type=int, default=85, choices=range(1,100), help="if no size is specified, length of generated words is determined by the average length in the dictionary, default is 85 percent")
    parser.add_argument("-m", "--max-attempts", metavar='NUM', type=int, default=50, help="specify the number of tries to generate a new word before throwing an error")
    parser.add_argument("--alpha", metavar='FILE', type=str, help="specify the alphabet file (alphabet is deduced from the dictionary if not specified)")
    parser.add_argument("-w", "--write", metavar='FILE', type=str, help="write the processed dictionary in the specified file")
    parser.add_argument("-o", "--output", metavar='FILE', type=str, help="write generated words in the specified file")
    parser.add_argument("--nb-columns", metavar='NUM', type=int, default=1, help="specify the number of columns tu use to display the generated words")
    parser.add_argument("-f", "--force", action='store_true', help="remove from the dictionary every word with at least one letter not in the alphabet (ignored if --alpha is absent)")
    parser.add_argument("-l", "--lowercase", action='store_true', help="lowercase every word from the dictionary")
    parser.add_argument("--print-acronyms", action='store_true', help="print acronyms from the dictionary to stdout")
    parser.add_argument("--print-plural", metavar='LANG', type=str, help="print to sdout the plural words whose singular is in the dictionary (depends on the language only FR is available yet)")
    parser.add_argument("--no-acronyms", action='store_true', help="remove acronyms from the dictionary")
    parser.add_argument("--no-plural", metavar='LANG', type=str, help="remove plural words from the dictionary")

    args = parser.parse_args()


    # getting dictionary
    dictionary = process_dictionary(open_dictionaries(args.dict))

    if args.print_acronyms:
        print_acronyms (dictionary)

    if args.print_plural is not None:
        print_plural_words (dictionary, args.print_plural)

    if args.no_acronyms:
        dictionary = remove_acronyms(dictionary)

    if args.lowercase:
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

        if '' in alphabet:
            alphabet.remove('')
        alphabet.append(find_separator(alphabet))

        matrix = build_ND_matrix(dictionary, alphabet, args.dim)

        word_list = []

        # size processing
        min_len = 0
        max_len = maxsize
        if args.size is not None:
            if ':' == args.size:
                pass
            elif not ':' in args.size:
                min_len = max(int(args.size), min_len)
                max_len = min(int(args.size), max_len)
            elif args.size.startswith(':'):
                max_len = int(args.size[1:])
            elif args.size.endswith(':'):
                min_len = int(args.size[:-1])
            else:
                min_len = max(int(args.size.split(':')[0]), min_len)
                max_len = min(int(args.size.split(':')[-1]), max_len)
            if max_len < min_len:
                raise Exception(f"size value error: {min_len} is greater than {max_len}")
        else:
            (min_len, max_len) = get_average_size(dictionary, args.average_size)

        # word generation
        failed_attempts = 0
        error = None
        nb_word_to_gen = args.gen
        while len(word_list) != nb_word_to_gen:
            word = generate_word_ND(matrix, alphabet, args.prefix, args.dim)
            # check word compliancy
            if len(word) < min_len or max_len < len(word):
                failed_attempts += 1
                if failed_attempts >= args.max_attempts:
                    error = 'size not compliant'
            elif args.new and word in dictionary:
                failed_attempts += 1
                if failed_attempts >= args.max_attempts:
                    error = 'word already in dictionary'
            elif word in word_list:
                failed_attempts += 1
                if failed_attempts >= args.max_attempts:
                    error = 'word already generated'
            else:
                word_list.append(word)
                failed_attempts = 0

            if error is not None:
                raise Exception(f"maximum number of attempts exceeded: generation failed {args.max_attempts} times in a raw, maybe this value with --max-attempts, last failure due to {error}")

        if args.capitalize:
            word_list = [word.capitalize() for word in word_list]

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

        if args.output is not None:
            filename = args.output
            write_generated_words(output_words, filename)
        else:
            print (output_words)
