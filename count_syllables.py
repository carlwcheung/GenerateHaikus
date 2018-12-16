"""
Count syllables in words using NLTK and associated CMU corpus
"""

from nltk.corpus import cmudict
import sys
from string import punctuation
import json

# load dictionary of words in haiku corpus but not in cmudict
with open('missing_words.json') as f:
    missing_words = json.load(f)

cmudict = cmudict.dict()

def count_syllables(words):

    # prep words for cmudict corpus
    words = words.replace('-', ' ')
    words = words.lower().split()
    number_syllables = 0
    for word in words:
        word = word.strip(punctuation)
        if word.endswith("'s")or word.endswith("’s"):
            word = word[:-2]
        if word in missing_words:
            number_syllables += missing_words[word]
        else:
            for phonemes in cmudict[word][0]:
                for phoneme in phonemes:
                    if phoneme[-1].isdigit():
                        number_syllables += 1
    return number_syllables

def main():
    while True:
        print("Syllable Counter")
        word = input("Enter word or phrase else press Enter to Exit: ")
        if word == '':
            sys.exit()

        try:
            number_syllables = count_syllables(word)
            print("number of syllables in {} is: {}"
                  .format(word, number_syllables))
            print()
        except KeyError:
            print("Word not found.  Try again.\n", file=sys.stderr)

if __name__ == '__main__':
    main()
