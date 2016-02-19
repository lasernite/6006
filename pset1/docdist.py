#!/usr/bin/python

import string
import sys
import math
    # math.acos(x) is the arccosine of x.
    # math.sqrt(x) is the square root of x.

# global variables needed for fast parsing
# translation table maps upper case to lower case and punctuation to spaces
translation_table = string.maketrans(string.punctuation+string.uppercase[0:26],
                                     " "*len(string.punctuation)+string.lowercase[0:26])


def count_frequency(word_list):
    D = {}
    for new_word in word_list:
        if new_word in D:
            D[new_word] = D[new_word]+1
        else:
            D[new_word] = 1
    return D.items()

def vector_angle(L1,L2):
    numerator = inner_product(L1,L2)
    denominator = math.sqrt(inner_product(L1,L1)*inner_product(L2,L2))
    return math.acos(numerator/denominator)

def inner_product(L1,L2):
    sum = 0.0
    for word1, count1 in L1:
        for word2, count2 in L2:
            if word1 == word2:
                sum += count1 * count2
    return sum

def extract_words(filename):
    """
    Return a list of words from a file
    """
    try:
        f = open(filename, 'r')
        doc = f.read()
        lines = doc.translate(translation_table)
        return lines.split()
    except IOError:
        print "Error opening or reading input file: ",filename
        sys.exit()

##############################################
## Part a. Count the frequency of each word ##
##############################################
def doc_dist(word_list1, word_list2):
    """
    Returns a float representing the document distance 
    in radians between two files when given the list of
    words from both files
    """
    word_frequency1 = count_frequency(word_list1)
    word_frequency2 = count_frequency(word_list2)
    return vector_angle(word_frequency1, word_frequency2)

##############################################
## Part b. Count the frequency of each pair ##
##############################################
def pair_count_frequency(word_list):
    D = {}
    for i in range(len(word_list) - 1):
        pair = word_list[i] + word_list[i+1]
        if pair in D:
            D[pair] = D[pair]+1
        else:
            D[pair] = 1
    return D.items()

def doc_dist_pairs(word_list1, word_list2):
    """
    Returns a float representing the document distance
    in radians between two files based on unique 
    consecutive pairs of words when given the list of
    words from both files
    """
    word_frequency1 = pair_count_frequency(word_list1)
    word_frequency2 = pair_count_frequency(word_list2)
    return vector_angle(word_frequency1, word_frequency2)

#############################################################
## Part c. Count the frequency of the 50 most common words ##
#############################################################
def doc_dist_50(word_list1, word_list2):
    """
    Returns a float representing the document distance
    in radians between two files based on the 
    50 most common unique words when given the list of
    words from both files
    """
    word_frequency1 = count_frequency(word_list1)
    word_frequency2 = count_frequency(word_list2)

    words_50_1 = sorted(word_frequency1, key = lambda x: (-x[1], x[0]))
    words_50_2 = sorted(word_frequency2, key = lambda x: (-x[1], x[0]))

    return vector_angle(words_50_1[0:50], words_50_2[0:50])

