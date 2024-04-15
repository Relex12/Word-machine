#!/bin/sh
./word-machine.py -h
./word-machine.py --help
./word-machine.py -d helloworld.txt
./word-machine.py --dict helloworld.txt
./word-machine.py -d helloworld.txt -g 1
./word-machine.py -d helloworld.txt --gen 1
./word-machine.py -d helloworld.txt -g 1 --dim 2
./word-machine.py -d helloworld.txt -g 1 -l -c
./word-machine.py -d helloworld.txt -g 1 --lowercase --capitalize
./word-machine.py -d helloworld.txt -g 1 --dim 2 -s 8:10
./word-machine.py -d helloworld.txt -g 1 --dim 2 --size 8:10
./word-machine.py -d helloworld.txt -g 1 --dim 2 -a 50
./word-machine.py -d helloworld.txt -g 1 --dim 2 --average 50
./word-machine.py -d helloworld.txt -g 1 --prefix HelloWorld
./word-machine.py -d helloworld.txt -g 1 --dim 2 -n
./word-machine.py -d helloworld.txt -g 1 --dim 2 --new
./word-machine.py -d helloworld.txt --alpha alphabet.txt
./word-machine.py -d helloworld.txt -w output_dictionary.txt
./word-machine.py -d helloworld.txt --write output_dictionary.txt
./word-machine.py -d helloworld.txt -g 1 -o output_words.txt
./word-machine.py -d helloworld.txt -g 1 --output output_words.txt
./word-machine.py -d helloworld.txt -f --alpha alphabet.txt
./word-machine.py -d helloworld.txt --force --alpha alphabet.txt
./word-machine.py -d helloworld.txt --print-acronyms
./word-machine.py -d helloworld.txt --print-plural FR
./word-machine.py -d helloworld.txt --no-acronyms
./word-machine.py -d helloworld.txt --no-plural FR
rm output_dictionary.txt output_words.txt
