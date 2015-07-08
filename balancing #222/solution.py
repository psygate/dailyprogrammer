#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

def main():
    '''Main method.'''
    words = ['CONSUBSTANTIATION', 'WRONGHEADED', 'UNINTELLIGIBILITY', 'SUPERGLUE']
    #words = ['STEAD']
    for word in words:
        tuple = try_balance(word)
        #Yup, empty tuples evaluate to false in an if expression.
        if tuple:
            print(tuple.left + " " + tuple.tippingpoint + " " + tuple.right + " - " + str(tuple.weight))
        else:
            print(word + ' DOES NOT BALANCE')

def weight_word(word):
    '''Converts a word to the letter value in the alphabet.
    A = 1, B = 2, C = 3, ..., Z = 26'''
    return [ord(letter) - ord('A') + 1 for letter in word]

def try_balance(word):
    '''Tries to balance a word around the tippingpoint'''
    weights = weight_word(word)
    #Distance for the left part to the tipping poing
    ldist = lambda tippingpoint, idx: tippingpoint - idx
    #Distance for a letter in the left part times the letter value
    lweight = lambda idx, left: left[idx] * ldist(tippingpoint, idx)

    #Distance for the right part to the tipping poing
    rdist = lambda tippingpoint, idx: idx - tippingpoint + 1
    #Distance for a letter in the right part times the letter value
    rweight = lambda idx, right: right[idx] * rdist(tippingpoint, tippingpoint + idx)

    for tippingpoint in range(0, len(weights)):
        #Named tuples are cool.
        WLR = namedtuple('WordLeftRightTuple', 'word tippingpoint left right weight')
        #Divide and conquer, split it into substrings around the tipping point
        # Excludes the letter at the tippingpoint
        left = weights[0:tippingpoint]
        right = weights[tippingpoint + 1:]

        # Caluclates the weight values for the left and right part of the word.
        lvalues = [lweight(idx, left) for idx in range(0, len(left))]
        rvalues = [rweight(idx, right) for idx in range(0, len(right))]

        lsum = sum(lvalues)
        rsum = sum(rvalues)

        if lsum == rsum:
            return WLR(word, word[tippingpoint], word[0:tippingpoint], word[tippingpoint + 1:], lsum)

    return ()

if __name__ == '__main__':
    main()
