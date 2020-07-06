# Word machine
A word generator from dictionary in Python

[TOC]

## Description

This repository provides a word generator based on statistical analysis of an input dictionary.

The algorithm is based on two main methods : the first one reads the dictionary and completes a matrix by counting how many times each a letter is followed by each other letter. The second algorithm uses these statistics to create a new word that looks like the words from the dictionary.



## Original idea

The generator and how it works have been imagined in the first place by David Louapre, a French science popularizer.

Please make sure to watch his video : [La machine à inventer des mots (avec Code MU) — Science étonnante #17](https://www.youtube.com/watch?v=YsR7r2378j0). It only has auto-generated subtitles and it talks about the French language, but I'm sure it will be OK.



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



## Run the demo

This section will be done soon.



## Input files specifications

The code requires exactly two input files.

The first file is an alphabet that contains every character that can be in the dictionary words. The alphabet file must be written as a single-space separated list of characters. **There must be a space after the final character**. All the characters must be on the first line, without carriage return. Upper and lower case letters must be both specified if needed. Each accent, digit or special character that is used have to be specified. Characters in the alphabet that are not used in the dictionary words are a small loss of memory, but the program still works. Characters from 'a' to 'z' and '-' are the often required.

The second file contains the dictionary that will be used. It must be represented as a carriage return separated list. **There should be no space between the word and the carriage return character**. LF and CRLF distinction should not be a problem. There is no need to order the words. Duplicated words are counted only once.



## Dictionary processing

As long as dictionary processing can be quite long, a few methods are given to help you manage it. These methods can lowcase every word in the dictionary, remove acronyms, remove duplicated words betwen singular and plural forms, even remove every word that contains at least one character that is not in the alphabet file (see the options below for more details). **The dictionary is always sorted and duplicates are removed.**



## Command line call and options

The word machine must be called from the command line running : `python word_machine.py [option]`.

The main options described below allow you to use the word machine effectively :

* `-alpha <file>` : loads the alphabet from the given file (if absent, command will use "alphabet.txt" as default)
* `-dict <file>` : loads the dictionary from the given file (if absent, command will use "dictionary.txt" as default)
* `-gen <number>` : generates as many words as requested (if absent, command will only process the dictionary)
* `-force` : removes from the dictionary every word with at least one character not in the alphabet



The following options allow you to more finely manage dictionary processing :

* `-low-case` : lowcases every word from the dictionary
* `-print-acronyms` : prints every acronyms (acronym = uppercase only words)
* `-print-plural <lang>` : prints duplicated words betwen singular and plural forms (non plural words could be removed)
* `-no-acronyms` : removes every acronyms from the dictionary 
* `-no-plural <lang>` : removes duplicated words betwen singular and plural forms (non plural words could be removed)
* `-write <file>` : writes the processed dictionary in the given file (if no file, "output_dictionary.txt" is default)

For the `-print-plural` and `-no-plural` options, please notice that only *"fr"* language is available for now.



The following options allow you to generate words with more parameters (they are ignored if -gen option is absent) :

* `-size <number>` : generates words of the required length only
* `-prefix <str>` : generates words with the given string as prefix
* `-new` : generates words that are not in the input dictionary
* `-output <file>` : writes the generated words in the given file (if no file, "generated_words.txt" is default)



## A bit deeper in the code

As the code have been developed on Atom, the input files can contain a final `'\n'` character. They are systematically removed when the files are loaded. Every eventual empty word (`''`) (corresponding to a white line) is removed when the dictionary is loaded.

An empty character is automatically added to the alphabet. This `''` character is used for letters that are at the beginning or at the end a word.

The built matrix is actually three dimensional, so it can read two characters before instead of one. For example, when the word *"age"* is ridden, the values in the boxes `['']['']['a']`, `['']['a']['g']`, `['a']['g']['e']`, `['g']['e']['']` and `['e']['']['']` from the matrix are increased.

A good example of why this is needed is the double letter probability. If a double "R" or "L" is quite common, it is very rare to see three R following each other.

The code provides methods for two dimensional matrix, but the results are pretty dismal.



## How to improve the project

* A four-dimensional matrix implementation should be done soon. But a good way to improve the code would be to implement an n-dimensional matrix, witch could go for any n value. 
  * Be careful however, a too large n value could hypothetically ruin the generator, by creating only words that already are in the dictionary (the limit value of n should vary with the size of the dictionary). Also, the minimum number of characters in generated word equals the dimension of the matrix minus one.
* There is currently no method to generate words with a specific suffix. A remnant of function can be found in the code, but you will have to build the matrix again, from the end to the beginning of the words.
* If you want, you can add plural rules in *print_plural_words()* and *remove_plural_words()* from your language, only french is currently provided.
* The matrix can't be visualised for the moment.  Printing the matrix as a two-dimensional table in a picture file would be awesome. You will probably need the *matplotlib.pyplot* method. As a starting point, you can use an interpolation of the existing matrix, or create the two-dimensional matrix and visualize it.



As this repository probably won't be very active in the long term future, please message me be email to coordinate an eventual Pull Request.



## Python version

As long as the `ramdon.choices()` method is used to create the words, Python 3.6 or more is required.



## License

The project is a small one. The code is given to the GitHub Community for free, only under the MIT License, that is not too restrictive.
