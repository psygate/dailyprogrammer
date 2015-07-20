#!/usr/bin/enc python
# -*- coding: utf-8 -*-

import sys, requests, os, codecs, re, operator, string, pprint
from functools import reduce
from collections import OrderedDict

def download_base_book():
    '''This will download Twenty Thousand Leagues Under the Seas
    if you don't have it already.'''

    with codecs.open('20k.txt', 'w', 'utf-8') as bookfile:
        addr = 'https://www.gutenberg.org/cache/epub/164/pg164.txt'
        response = requests.get(addr)
        bookfile.write(response.text)

def build_letter_map(filename, depth):
    '''Builds a letter map from the specified file'''
    lmap = dict()
    with codecs.open('20k.txt', 'r', 'utf-8') as bookfile:
        for word in filter(is_valid_word, [
        # Map the lines to a list of words
            word for line in bookfile for word in to_words(line)]):
            # Update the current letter map with the word
            build_map(word, depth, lmap)

    return lmap

def build_map(word, depth, lmap):
    '''Adds the letters of the word to depth depth with to the provided map'''
    for idx in range(0, len(word) - depth  + 1):
        substr = word[idx:idx + depth]
        assert len(substr) == depth
        curmap = lmap

        for char in substr:
            if not char in curmap.keys():
                curmap[char] = OrderedDict()
            curmap = curmap[char]

    return lmap

def reduce_maps(lmaps, rmaps):
    '''Reduces two letter maps to one.'''
    comb = lmaps.copy()
    #keep track of where we are in the dictionary
    stack = list()
    stack.append((comb, rmaps))

    while stack:
        combmap, rmap = stack.pop()
        combmap.update(rmap)
        for key in rmap.keys():
            stack.append((combmap[key], rmap[key]))


    return comb

def to_words(line):
    '''splits a line to words containing only lowercase letters'''
    # Remove punctuation.
    for punctuation in string.punctuation:
        line = line.replace(punctuation, "")

    # split around whitespaces
    whitespace = re.compile("\s+")

    candidates = whitespace.split(line)

    return filter(lambda c: len(c) > 0, [candidate.lower() for candidate in candidates])


def is_valid_word(word):
    '''Checks if word is a valid word (only lowercase letters.)'''
    for char in word:
        if not char in string.ascii_lowercase:
            return False

    return True

def can_build(word, lettermap, depth):
    '''Checks if a word can be built with the provided letter map'''
    for idx in range(0, len(word) - depth  + 1):
        substr = word[idx:idx + depth]
        assert len(substr) == depth
        curmap = lettermap

        for char in substr:
            if not char in curmap.keys():
                return False
            curmap = curmap[char]

    return True

def main():
    '''Main method.'''
    # Get our reference book if we don't have it already.
    if not os.path.isfile("20k.txt"):
        download_base_book()

    # How deep we want to build the map
    mapdepth = 3

    lettermap = build_letter_map("20k.txt", mapdepth)
    with codecs.open("challenge.txt", 'r', 'utf-8') as challenge:
        for line in challenge:
            if reduce(lambda a,b: a and b, [can_build(word, lettermap, mapdepth) for word in to_words(line)]):
                print(line)


if __name__ == '__main__':
    main()
