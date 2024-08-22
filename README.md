# Word-machine
A word generator from dictionary in Python

![](https://img.shields.io/github/license/Relex12/Word-Machine) ![](https://img.shields.io/github/repo-size/Relex12/Word-Machine) ![](https://img.shields.io/github/languages/top/Relex12/Word-Machine) ![](https://img.shields.io/github/last-commit/Relex12/Word-Machine) ![](https://img.shields.io/github/stars/Relex12/Word-Machine)

Check out on GitHub

[![Word-Machine](https://github-readme-stats.vercel.app/api/pin/?username=Relex12&repo=Word-Machine)](https://github.com/Relex12/Word-Machine)

Documentation:

* [`anagram.py`](https://relex12.github.io/Word-machine/doc/anagram.html)
* [`dictionary.py`](https://relex12.github.io/Word-machine/doc/dictionary.html)
* [`generation.py`](https://relex12.github.io/Word-machine/doc/generation.html)
* [`word-machine.py`](https://relex12.github.io/Word-machine/doc/word-machine.html)

---

## Summary

* [Word-machine](#word-machine)
    * [Description](#description)
    * [Original idea](#original-idea)
    * [Run the demo](#run-the-demo)
    * [Dictionary processing](#dictionary-processing)
    * [Results](#results)
    * [Command-line interface options](#command-line-interface-options)
    * [Run the tests](#run-the-tests)
    * [Introduction to the code](#introduction-to-the-code)
    * [Documentation](#documentation)
    * [How to improve ?](#how-to-improve-)
    * [Python version](#python-version)
    * [License](#license)

<!-- table of contents created by Adrian Bonnet, see https://github.com/Relex12/Markdown-Table-of-Contents for more -->

## Description

word-machine is a word generator based on statistical analysis of an input dictionary.

The algorithm is based on two main methods : the first one reads the dictionary and completes a matrix by counting how many times each a letter is followed by each other letter. The second method uses these statistics to create a new word that looks like the words from the dictionary.

## Original idea

The generator and how it works have been imagined in the first place by David Louapre, a French science popularizer.

Please make sure to watch his video : [La machine à inventer des mots (avec Code MU) — Science étonnante #17](https://www.youtube.com/watch?v=YsR7r2378j0). It only has auto-generated subtitles and it talks about the French language, but I'm sure it will be OK.

## Run the demo

One word-machine is installed, you should be able to run `python3 word-machine.py -d helloworld.txt -g 1`, the output will be `HelloWorld!`.

## Dictionary processing

As long as dictionary processing can be quite long, a few methods are given to help you manage it. These methods can low-case every word in the dictionary, remove acronyms, remove duplicated words between singular and plural forms, even remove every word that contains at least one character that is not in the alphabet file (see the options below for more details). **The dictionary is always sorted and duplicates are removed.**

Every line from the dictionary starting with the `#` character will be treated as a **comment**.

## Results

English-version example will arrive soon.

Using a French dictionary of more than 20,000 words, here an example of generated words :

```
racque
férire
tréterisés
hoistelas
brissit
sousernérarent
pes
prittérent
gramosaibule
saingulégayant
pritéliser
juser
ine
larron
honseme
fréconavueilluseme
mardusemés
prouté
se
```

## Command-line interface options

Usage and options are given by `./word-machine.py --help`.

```
usage: word-machine.py [-h] [-g NUM] [-a STR] [-d [FILE [FILE ...]]] [--dim NUM] [-c] [-s SIZE] [-n] [-p PREFIX] [--length-range PERCENT] [--max-attempts NUM] [-w STR] [-r NUM] [-v NUM] [--match-case]
                       [--nb-limit NUM] [--disable-progress-bar] [--write FILE] [-o FILE] [--nb-columns NUM] [-l] [--alpha FILE] [-f] [--print-acronyms] [--print-plural LANG] [--no-acronyms]
                       [--no-plural LANG]

optional arguments:
  -h, --help            show this help message and exit
  -g NUM, --gen NUM     generate as many words as specified
  -a STR, --anagram STR
                        give the best anagrams of the specified word
  -d [FILE [FILE ...]], --dict [FILE [FILE ...]]
                        specify the dictionary files
  --dim NUM             use the specified dimension for the matrix (between 2 and 3) (default: 3)
  -c, --capitalize      capitalize output words

generation arguments:
  -s SIZE, --size SIZE  specify the length of generated words. SIZE can be 'NUM' (equals) 'NUM:' (less than) ':NUM' (more than) 'NUM:NUM' (between) or ':' (any)
  -n, --new             generate words that are not in the dictionary and not already generated
  -p PREFIX, --prefix PREFIX
                        specify a prefix for all generated words
  --length-range PERCENT
                        percentage of words in the dictionary used to get the word length range (if --size not specified) (default: 85)
  --max-attempts NUM    specify the number of tries to generate a new word before throwing an error (default: 50)
  --match-case          give anagrams matching case

anagram arguments:
  -w STR, --wildcard STR
                        string of characters that can be added to the anagram
  -r NUM, --repeat NUM  number of times a wildcard character can be used (must be kept really low) (default: 1)
  -v NUM, --view NUM    number of anagrams displayed (default: 30)
  --nb-limit NUM        limit on the number of possible anagrams (default: 100000000)
  --disable-progress-bar
                        disable progress bars during anagrams generation and scoring

miscellaneous:
  --write FILE          write the processed dictionary in the specified file
  -o FILE, --output FILE
                        write generated words in the specified file
  --nb-columns NUM      specify the number of columns tu use to display the generated words
  -l, --lowercase       lowercase every word from the dictionary
  --alpha FILE          specify the alphabet file (alphabet is deduced from the dictionary if not specified)
  -f, --force           remove from the dictionary every word with at least one letter not in the alphabet (ignored if --alpha is absent)
  --print-acronyms      print acronyms from the dictionary to stdout
  --print-plural LANG   print to sdout the plural words whose singular is in the dictionary (depends on the language only FR is available yet)
  --no-acronyms         remove acronyms from the dictionary
  --no-plural LANG      remove plural words from the dictionary
```

## Run the tests

The `test.sh` file lists unit tests for all option.

On Unix, run `sh test.sh` to run each test, there should be no error.

Note that those are not unit tests, they only verify that every argument to the command line provides an error free execution, but it does not mean that the behavior is correct.

## Introduction to the code

As the code have been developed on Atom, the input files can contain a final `'\n'` character. They are systematically removed when the files are loaded. Every eventual empty word (`''`) (corresponding to a white line) is removed when the dictionary is loaded.

An empty character is automatically added to the alphabet. A special character known as the separator is used for letters that are at the beginning or at the end a word.

The built matrix is actually multi dimensional, so it can read multiple characters before instead of one. For example with a three dimension matrix, when the word *"age"* is ridden, the values in the boxes `[separator+separator]['a']`, `[separator+'a']['g']`, `['ag']['e']`, `['ge'][separator]` and `['e'+separator][separator]` from the matrix are increased.

A good example of why this is needed is the double letter probability. If a double "R" or "L" is quite common, it is very rare to see three R following each other.

The code provides methods for two dimensional matrix, but the results are pretty dismal.

## Documentation

The documentation is available in the `doc/` folder.

The documentation is generated by [pdoc3](https://pdoc3.github.io/pdoc/), it can be rebuilt by running `pdoc --html -o doc/ *.py` in the main directory.

## How to improve ?

* There is currently no method to generate words with a specific suffix. A remnant of function can be found in the code, but you will have to build the matrix again, from the end to the beginning of the words.
* If you want, you can add plural rules in `print_plural_words()` and `remove_plural_words()` from your language, only french is currently provided.
* The matrix can't be visualized for the moment.  Printing the matrix as a two-dimensional table in a picture file would be awesome. You will probably need the `matplotlib.pyplot()` method. As a starting point, you can use an interpolation of the existing matrix, or create the two-dimensional matrix and visualize it.

Feel free to open a Pull Request.

## Python version

As long as the `ramdon.choices()` method is used to create the words, Python 3.6 or more is required.

## License

The project is a small one. The code is given to the GitHub Community for free, only under the MIT License, that is not too restrictive.
