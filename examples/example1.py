#!/bin/env python
# -*- coding: utf-8 -*-
# Code modified by Rachael Tatman, at the University of Washington. 
# Contact: rctatman@uw.edu

# This code will read in files from the Corpus NGT and produce token counts from the right and left hands respectively.

import glob     # Import glob to easily loop over files
import pympi    # Import pympi to work with elan files
import string   # Import string to get the punctuation data
import re # Import regular expressions

# Define some variables for later use
corpus_root = '/home/usr/ngtCorpus/corpusngt_eaf_r2_public/CorpusNGT_eaf_r2_public'
leftHandTierName = ["GlossL S1",  "GlossL S2"]
rightHandTierName = ["GlossR S1",  "GlossL S2"]

# Initialize the frequency dictionaries
frequency_dict_left = {}
frequency_dict_right = {}
number = 0

# .eaf method documatination: http://dopefishh.github.io/pympi/docs_1.1/Elan.html
# Loop over all elan files the corpusroot subdirectory called eaf
for file_path in glob.glob('{}/*/*.eaf'.format(corpus_root)):
    # Initialize the elan file
    eafob = pympi.Elan.Eaf(file_path)
    # Loop over all the defined tiers that contain orthography
    for ort_tier in leftHandTierName:
        # If the tier is not present in the elan file spew an error and
        # continue. This is done to avoid possible KeyErrors
        if ort_tier not in eafob.get_tier_names():
            print 'WARNING!!!'
            print 'One of the ortography tiers is not present in the elan file'
            print 'namely: {}. skipping this one...'.format(ort_tier)
        # If the tier is present we can loop through the annotation data
        else:
            for annotation in eafob.get_annotation_data_for_tier(ort_tier):
                # We are only interested in the utterance
                utterance = annotation[2]
                # Split, by default, splits on whitespace thus separating words
                words = utterance.split()
                # For every word increment the frequency
                for word in words:
                    # Remove the possible punctuation
                    for char in string.punctuation:
                        word = word.replace(char, '')
                    # Convert to lowercase
                    word = word.lower()
                    # Increment the frequency, using the get method we can
                    # avoid KeyErrors and make sure the word is added when it
                    # wasn't present in the frequency dictionary
                    frequency_dict_left[word] = frequency_dict_left.get(word, 0) + 1
                      # Loop over all the defined tiers that contain orthography
    # Open an output file in the current directory to write the data to left hand
    n = re.split('/\w*.eaf', file_path)[0]
    name = 'word_frequencies_left.txt'
    new_name = '{}/' + str(number) + name
    output_file_left = new_name .format(n)
    with open(output_file_left, 'w') as output_file_left:
        # Loop throught the words with their frequencies, we do this sorted because
        # the file will then be more easily searchable
        for word, frequency in sorted(frequency_dict_left.items()):
            # We write the output separated by tabs
            output_file_left.write('{}\t{}\n'.format(word, frequency))
    for ort_tier in rightHandTierName:
        # If the tier is not present in the elan file spew an error and
        # continue. This is done to avoid possible KeyErrors
        if ort_tier not in eafob.get_tier_names():
            print 'WARNING!!!'
            print 'One of the ortography tiers is not present in the elan file'
            print 'namely: {}. skipping this one...'.format(ort_tier)
        # If the tier is present we can loop through the annotation data
        else:
            for annotation in eafob.get_annotation_data_for_tier(ort_tier):
                # We are only interested in the utterance
                utterance = annotation[2]
                # Split, by default, splits on whitespace thus separating words
                words = utterance.split()
                # For every word increment the frequency
                for word in words:
                    # Remove the possible punctuation
                    for char in string.punctuation:
                        word = word.replace(char, '')
                    # Convert to lowercase
                    word = word.lower()
                    # Increment the frequency, using the get method we can
                    # avoid KeyErrors and make sure the word is added when it
                    # wasn't present in the frequency dictionary
                    frequency_dict_right[word] = frequency_dict_right.get(word, 0) + 1
    # Open an output file in the current directory to write the data to rigth hand
    n = re.split('/\w*.eaf', file_path)[0]
    name = 'word_frequencies_right.txt'
    new_name = '{}/' + str(number) + name
    number =  number + 1
    output_file_right = new_name .format(n)
    with open(output_file_right, 'w') as output_file_right:
        # Loop throught the words with their frequencies, we do this sorted because
        # the file will then be more easily searchable
        for word, frequency in sorted(frequency_dict_right.items()):
            # We write the output separated by tabs
            output_file_right.write('{}\t{}\n'.format(word, frequency))
