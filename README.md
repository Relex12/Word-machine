# Word-machine
A word generator from dictionary in Python

![](https://img.shields.io/github/license/Relex12/Word-Machine) ![](https://img.shields.io/github/repo-size/Relex12/Word-Machine) ![](https://img.shields.io/github/languages/top/Relex12/Word-Machine) ![](https://img.shields.io/github/last-commit/Relex12/Word-Machine) ![](https://img.shields.io/github/stars/Relex12/Word-Machine)

Check out on GitHub

[![Word-Machine](https://github-readme-stats.vercel.app/api/pin/?username=Relex12&repo=Word-Machine)](https://github.com/Relex12/Word-Machine)

Documentation:

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
usage: word-machine.py [-h] [-v] [-d [FILE ...]] [-g NUM] [--dim NUM] [-n] [-p PREFIX] [-c] [-s SIZE] [-a PER] [-m NUM] [--alpha FILE] [-w FILE] [-o FILE] [--nb-columns NUM] [-f]
                       [-l] [--print-acronyms] [--print-plural LANG] [--no-acronyms] [--no-plural LANG]

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d [FILE ...], --dict [FILE ...]
                        specify the dictionary files
  -g NUM, --gen NUM     generate as many words as specified (option required for every option below)
  --dim NUM             use the specified dimension for the matrix (between 2 and 3)
  -n, --new             generate words that are not in the dictionary and not already generated
  -p PREFIX, --prefix PREFIX
                        specify a prefix for all generated words
  -c, --capitalize      capitalize generated words
  -s SIZE, --size SIZE  specify the length of generated words. SIZE can be 'NUM' (equals) 'NUM:' (less than) ':NUM' (more than) 'NUM:NUM' (between) or ':' (any)
  -a PER, --average-size PER
                        if no size is specified, length of generated words is determined by the average length in the dictionary, default is 85 percent
  -m NUM, --max-attempts NUM
                        specify the number of tries to generate a new word before throwing an error
  --alpha FILE          specify the alphabet file (alphabet is deduced from the dictionary if not specified)
  -w FILE, --write FILE
                        write the processed dictionary in the specified file
  -o FILE, --output FILE
                        write generated words in the specified file
  --nb-columns NUM      specify the number of columns tu use to display the generated words
  -f, --force           remove from the dictionary every word with at least one letter not in the alphabet (ignored if --alpha is absent)
  -l, --lowercase       lowercase every word from the dictionary
  --print-acronyms      print acronyms from the dictionary to stdout
  --print-plural LANG   print to sdout the plural words whose singular is in the dictionary (depends on the language only FR is available yet)
  --no-acronyms         remove acronyms from the dictionary
  --no-plural LANG      remove plural words from the dictionary
```

## Run the tests

The `test/test-list.txt` file lists unit tests for all option.

On Unix, run `bash test/test-list.txt` to run each test, there should be no error.

Note that those are not unit tests, they only verify that every argument to the command line provides an error free execution, but it does not mean that the behavior is correct.

## Introduction to the code

As the code have been developed on Atom, the input files can contain a final `'\n'` character. They are systematically removed when the files are loaded. Every eventual empty word (`''`) (corresponding to a white line) is removed when the dictionary is loaded.

An empty character is automatically added to the alphabet. This `''` character is used for letters that are at the beginning or at the end a word.

The built matrix is actually three dimensional, so it can read two characters before instead of one. For example, when the word *"age"* is ridden, the values in the boxes `['']['']['a']`, `['']['a']['g']`, `['a']['g']['e']`, `['g']['e']['']` and `['e']['']['']` from the matrix are increased.

A good example of why this is needed is the double letter probability. If a double "R" or "L" is quite common, it is very rare to see three R following each other.

The code provides methods for two dimensional matrix, but the results are pretty dismal.

## Documentation

The documentation is available in the `doc/` folder.

The documentation is generated by [pdoc3](https://pdoc3.github.io/pdoc/), it can be rebuilt by running `pdoc --html -o doc/ *.py` in the main directory.

## How to improve ?

* A four-dimensional matrix implementation should be done soon. But a good way to improve the code would be to implement an n-dimensional matrix, witch could go for any n value.
  * Be careful however, a too large n value could hypothetically ruin the generator, by creating only words that already are in the dictionary (the limit value of n should vary with the size of the dictionary). Also, the minimum number of characters in generated word equals the dimension of the matrix minus one.
* There is currently no method to generate words with a specific suffix. A remnant of function can be found in the code, but you will have to build the matrix again, from the end to the beginning of the words.
* If you want, you can add plural rules in `print_plural_words()` and `remove_plural_words()` from your language, only french is currently provided.
* The matrix can't be visualized for the moment.  Printing the matrix as a two-dimensional table in a picture file would be awesome. You will probably need the `matplotlib.pyplot()` method. As a starting point, you can use an interpolation of the existing matrix, or create the two-dimensional matrix and visualize it.

To coordinate an eventual Pull Request, please message me be email.

## Python version

As long as the `ramdon.choices()` method is used to create the words, Python 3.6 or more is required.

## License

The project is a small one. The code is given to the GitHub Community for free, only under the MIT License, that is not too restrictive.
