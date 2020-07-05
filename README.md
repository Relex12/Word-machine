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

This section will be done in the next commit.

## Run the demo

This section will be done in the next commit.

## Input files specifications

The code requires exactly two input files.

The first file is an alphabet that contains every character that can contained is the dictionary words. The alphabet file must be written as a single space separated list of characters. All the characters must be on the first line, without carriage return. Upper and lower case letters must be both specified if needed. Each accent, digit or special character that is used have to be specified. Characters in the alphabet that are not used in the dictionary words are a loss of memory space, but the program still works. 'a' to 'z' characters and '-' are the often required.

The second file contains the dictionary that will be used. It must be represented as a carriage return separated list. There should be no space between the word and the carriage return character. LF and CRLF distinction should not be a problem. There is no need to order the word. **Duplicated words are counted only once.**

## Dictionary processing

As dictionary processing can be quite long, a method is given to help you manage it. This method returns a new word dictionary, ordered and without duplicates, a list of words that could be duplicated between singular and plural forms, and a list of characters that have been found at least once in the dictionary and that are not in the alphabet file.

The list of words that could be duplicated between singular and plural forms is based on if the word already exists without the final 'S' or not. This might not work if you're using a language that does not necessarily includes an 'S' in the plural, such as German or French ("-al" and "-ail" words for example). These words are not removed since you might want to keep them.

## A bit deeper in the code

As the code have been developed on Atom, the input files can contain a final `'\n'` character. It is systematically removed when the files are loaded. Every eventual empty word (`''`) is removed when the dictionary is loaded.

An empty character is automatically added to the alphabet. This `''` character is used for letters that are at the beginning or at the end a word.

The built matrix is actually three dimensional, so it can read two characters before instead of one. For example, when the word "age" is ridden, the values in the `['']['']['a']`, `['']['a']['g']`, `['a']['g']['e']`, `['g']['e']['']` and `['e']['']['']` boxes in the matrix are increased.

A good example of why this is needed is the double letter probability. If a double "R" or "L" is quite common, it is very rare to see three R following each other.

The code provides methods for two dimensional matrix, but the results are pretty dismal.

Technically, increasing the dimension of the matrix is always a good way to improve the results.

## How to improve the code

A four-dimensional matrix implementation should be done soon.

A very very good way to improve the code would be to implement n-dimensional matrix, witch could go for any n value.

Another way to improve the quality would be to create a method that enable the visualization of the matrix. It could use an interpolation of the existing matrix, or create the two-dimensional matrix and visualize it.

As this repository probably won't be very active, please message me be email to coordinate an eventual Pull Request.

## Python version

As long as the `ramdon.choices()` method is used to create the words, Python 3.6 or more is required.

## License

The project is a small one. The code is given to the GitHub Community for free, only under th MIT License, that is not too restrictive.
