#!/usr/bin/env python3

"""
## This module allows you to **execute** the code and manages command-line options.
"""

from argparse import ArgumentParser

from anagram import *
from dictionary import *
from generation import *

#############################
# Main zone : executed code #
#############################

if __name__ == '__main__':

    ########################
    # Arguments processing #
    ########################

    parser = ArgumentParser()

    parser.add_argument("-g", "--gen", metavar='NUM', type=int, help="generate as many words as specified")
    parser.add_argument("-a", "--anagram", metavar='STR', type=str, help="give the best anagrams of the specified word")
    parser.add_argument("-d", "--dict", metavar='FILE', nargs='*', help="specify the dictionary files")
    parser.add_argument("--dim", metavar='NUM', type=int, choices=range(2,6), default=3, help="use the specified dimension for the matrix (between 2 and 3) (default: %(default)s)")
    parser.add_argument("-c", "--capitalize", action='store_true', help="capitalize output words")

    gen_group = parser.add_argument_group("generation arguments")
    gen_group.add_argument("-s", "--size", help="specify the length of generated words. SIZE can be 'NUM' (equals) 'NUM:' (less than) ':NUM' (more than) 'NUM:NUM' (between) or ':' (any)")
    gen_group.add_argument("-n", "--new", action='store_true', help="generate words that are not in the dictionary and not already generated")
    gen_group.add_argument("-p", "--prefix", type=str, default='', help="specify a prefix for all generated words")
    gen_group.add_argument("--length-range", metavar='PERCENT', type=int, default=85, choices=range(1,100), help="percentage of words in the dictionary used to get the word length range (if --size not specified) (default: %(default)s)")
    gen_group.add_argument("--max-attempts", metavar='NUM', type=int, default=50, help="specify the number of tries to generate a new word before throwing an error (default: %(default)s)")

    ana_group = parser.add_argument_group("anagram arguments")
    ana_group.add_argument("-w", "--wildcard", metavar='STR', type=str, default='', help="string of characters that can be added to the anagram")
    ana_group.add_argument("-r", "--repeat", metavar='NUM', type=int, default=1, help="number of times a wildcard character can be used (must be kept really low) (default: %(default)s)")
    ana_group.add_argument("-v", "--view", metavar='NUM', type=int, default=30, help="number of anagrams displayed (default: %(default)s)")
    gen_group.add_argument("--match-case", action='store_true', help="give anagrams matching case")
    ana_group.add_argument("--nb-limit", metavar='NUM', type=int, default=10**8, help="limit on the number of possible anagrams (default: %(default)s)")
    ana_group.add_argument("--disable-progress-bar", action='store_true', help="disable progress bars during anagrams generation and scoring")

    misc_group = parser.add_argument_group("miscellaneous")
    misc_group.add_argument("--write", metavar='FILE', type=str, help="write the processed dictionary in the specified file")
    misc_group.add_argument("-o", "--output", metavar='FILE', type=str, help="write generated words in the specified file")
    misc_group.add_argument("--nb-columns", metavar='NUM', type=int, default=1, help="specify the number of columns tu use to display the generated words")
    misc_group.add_argument("-l", "--lowercase", action='store_true', help="lowercase every word from the dictionary")
    misc_group.add_argument("--alpha", metavar='FILE', type=str, help="specify the alphabet file (alphabet is deduced from the dictionary if not specified)")
    misc_group.add_argument("-f", "--force", action='store_true', help="remove from the dictionary every word with at least one letter not in the alphabet (ignored if --alpha is absent)")
    misc_group.add_argument("--print-acronyms", action='store_true', help="print acronyms from the dictionary to stdout")
    misc_group.add_argument("--print-plural", metavar='LANG', type=str, help="print to sdout the plural words whose singular is in the dictionary (depends on the language only FR is available yet)")
    misc_group.add_argument("--no-acronyms", action='store_true', help="remove acronyms from the dictionary")
    misc_group.add_argument("--no-plural", metavar='LANG', type=str, help="remove plural words from the dictionary")

    args = parser.parse_args()

    ###################################
    # Getting dictionary and alphabet #
    ###################################

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

    ###################
    # Misc processing #
    ###################

    if args.gen is not None or args.anagram is not None:

        if '' in alphabet:
            alphabet.remove('')
        alphabet.append(find_separator(alphabet))

        matrix = build_ND_matrix(dictionary, alphabet, args.dim)

        if args.size is not None:
            (min_len, max_len) = process_size(args.size)
        else:
            (min_len, max_len) = get_length_range(dictionary, args.length_range)

    ####################
    # Generating words #
    ####################

    if args.gen is not None:

        word_list = []

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
                raise Exception(f"maximum number of attempts exceeded: generation failed {args.max_attempts} times in a raw, maybe increase this value with --max-attempts, last failure due to {error}")

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

    ####################
    # Getting anagrams #
    ####################

    if args.anagram is not None:

        word = args.anagram.lower() if not args.match_case else args.anagram

        wildcards = args.repeat*args.wildcard.lower() if not args.match_case else args.repeat*args.wildcard
        wc_subsets = [str(''.join(str(i) for i in s)) for s in powerset(wildcards)]

        nb_words = 0
        for s in wc_subsets:
            nb_words += factorial(len(word+s))
        if nb_words > args.nb_limit:
            raise Exception(f"too many combinations error: {nb_words} possible words exeeds {args.nb_limit} limit")

        perms = []
        for s in wc_subsets:
            perms.extend(["".join(p) for p in permutations(word+s)])
            if not args.disable_progress_bar:
                progress_bar(count=len(perms),total=nb_words)
        perms = list(set(perms))

        scores = []
        progress = 0
        for p in perms:
            score = compute_score_ND(p, matrix, alphabet, args.dim)
            if score > 0:
                scores.append((p, score))
            progress+=1
            if not args.disable_progress_bar and ( progress % 100 == 0 or progress == len(perms) ):
                progress_bar(count=progress,total=len(perms))
        scores.sort(key=lambda x: x[1])

        for s in scores[-min(args.view, len(scores)):]:
            print (s[0].capitalize()) if args.capitalize else print (s[0].capitalize())
