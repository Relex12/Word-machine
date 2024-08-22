"""
## This module allows you to **score** anagrams.
"""

from itertools import permutations, chain, combinations
from math import factorial
from sys import stdout

from generation import *
from dictionary import *

def powerset(iterable):
    """
    powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    copied from: https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def progress_bar(count,total,size=60,sides="[]",full='#',empty='.',prefix=""):
    """
    copied from: https://github.com/Relex12/Simple-Progress-Bar
    """
    x = int(size*count/total)
    stdout.write("\r" + prefix + sides[0] + full*x + empty*(size-x) + sides[1] + ' ' + str(count).rjust(len(str(total)),' ')+"/"+str(total))
    if count==total:
        stdout.write("\r"+(size+20)*" "+"\r")

def compute_score_ND(word, matrix, alphabet, N):
    """
    `compute_score_ND()` compute the score of a word based on a matrix.

    * **word** (*str*): the word to score
    * **matrix** (*dict*): the matrix representing the probability of letter chaining each other
    * **alphabet** (*list*): the used alphabet (from input file or from dictionary)
    * **N** (*int*): the dimension of the matrix
    * **return** (*float*): the score of the word
    """
    separator = alphabet[-1]
    word = (N-1)*separator+word+(N-1)*separator
    score = 0
    for i in range(len(word)-N+1):
        matrix_value = matrix[word[i:i+N-1]][word[i+N-1]]
        if matrix_value == 0:
            return 0
        score += matrix_value
    return score/len(word)
