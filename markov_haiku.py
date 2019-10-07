"""
Produce new haiku from training corpus of existing haiku
"""
import sys
import logging
import random
from collections import defaultdict
from count_syllables import count_syllables

logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

def load_training_file(file):
    with open(file) as f:
        raw_haiku = f.read()
        return raw_haiku

def prep_training(raw_haiku):
    """
    Load string, remove newline
    Return list of words
    """
    word_list = raw_haiku.replace('\n', ' ').split()
    return word_list

def build_order1_markov(word_list):
    limit = len(word_list)-1
    order1_dict = defaultdict(list)
    for index, word in enumerate(word_list):
        if index < limit:
            suffix = word_list[index + 1]
            order1_dict[word].append(suffix)
    logging.debug("build_order1_markov results for \"sake\" = %s\n",
                  order1_dict['sake'])
    return order1_dict

def build_order2_markov(word_list):
    limit = len(word_list)-2
    order2_dict = defaultdict(list)
    for index, word in enumerate(word_list):
        if index < limit:
            key = word + ' ' + word_list[index + 1]
            suffix = word_list[index + 2]
            order2_dict[key].append(suffix)
    logging.debug("build_order2_markov results for \"sake jug\" = %s\n",
                  order2_dict['sake jug'])
    return order2_dict

def random_word(word_list):
    """
    Return random word and syllable count from training corpus
    Use this to begin haiku
    """
    chosen_word = random.choice(word_list)
    number_of_syllables = count_syllables(chosen_word)
    if number_of_syllables > 4:
        random_word(word_list)
    else:
        logging.debug("random word & syllables = %s %s\n", chosen_word, number_of_syllables)
        return (chosen_word, num_syls)

def word_after_single(prefix, suffix_order1, current_number_syllables, target_number_syllables):
    """
    Return all acceptable words in a corpus that follow a single word
    """
    usable_words = []
    suffixes = suffix_order1.get(prefix)
    if suffixes is not None:
        for candidate in suffixes:
            number_of_syllables = count_syllables(candidate)
            if current_number_syllables + number_of_syllables <= target_number_syllables:
                usable_words.append(candidate)
    logging.debug("accepted words after \"%s\" = %s\n",
                  prefix, set(accepted_words))
    return usable_words


def word_after_pair(prefix, suffix_order2, current_number_syllables, target_number_syllables):
    """
    Return all acceptable words in a corpus that follow a word pair
    """
    usable_words = []
    suffixes = suffix_order2.get(prefix)
    if suffixes is not None:
        for candidate in suffixes:
            number_of_syllables = count_syllables(candidate)
            if current_number_syllables + number_of_syllables <= target_number_syllables:
                usable_words.append(candidate)
    logging.debug("accepted words after \"%s\" = %s\n",
                  prefix, set(accepted_words))
    return usable_words

def generate_haiku_line(suffix_order1, suffix_order2, word_list,  end_previous_line, target_number_syllables):
    line = '2/3'
    syllables_in_line = 0
    current_line = []

    if len(end_previous_line) == 0:  # build first line
        line = '1'
        word, number_of_syllables = random_word(word_list)
        current_line.append(word)
        syllables_in_line += number_of_syllables
        word_choices = word_after_single(word, suffix_order11,
                                         syllables_in_line, target_number_syllables)
        while len(word_choices) == 0:
            prefix = random.choice(word_list)
            logging.debug("new random prefix = %s", prefix)
            word_choices = word_after_single(prefix, suffix_map_1,
                                             line_syls, target_syls)
        word = random.choice(word_choices)
        number_of_syllables = count_syllables(word)
        logging.debug("word & syllables = %s %s", word, number_of_syllables)
        syllables_in_line += number_of_syllables
        current_line.append(word)
        if syllables_in_line == target_number_syllables:
            end_previous_line.extend(current_line[-2:])
            return current_line, end_previous_line

    else:  # build lines 2 & 3
        current_line.extend(end_prev_line)

    while True:
        logging.debug("line = %s\n", line)
        prefix = current_line[-2] + ' ' + current_line[-1]
        word_choices = word_after_double(prefix, suffix_order2,
                                         syllables_in_line, target_number_syllables)
        while len(word_choices) == 0:
            index = random.randint(0, len(corpus) - 2)
            prefix = word_list[index] + ' ' + word_list[index + 1]
            logging.debug("new random prefix = %s", prefix)
            word_choices = word_after_double(prefix, suffix_order2,
                                             syllables_in_line, target_number_syllables)
        word = random.choice(word_choices)
        number_of_syllables = count_syllables(word)
        logging.debug("word & syllables = %s %s", word, number_syllables)

        if syllables_in_line + number_syllables > target_number_syllables:
            continue
        elif syllables_in_line + number_syllables < target_number_syllables:
            current_line.append(word)
            syllables_in_line += number_syllables
        elif syllables_in_line + number_syllables == target_number_syllables:
            current_line.append(word)
            break

    end_previous_line = []
    end_previous_line.extend(current_line[-2:])

    if line == '1':
        final_line = current_line[:]
    else:
        final_line = current_line[2:]

    return final_line, end_prevous_line


def main():
    """Give user choice of building a haiku or modifying an existing haiku."""
    intro = """\n
    A thousand monkeys at a thousand typewriters...
    or one computer...can sometimes produce a haiku.\n"""
    print("{}".format(intro))

    raw_haiku = load_training_file("train.txt")
    word_list = prep_training(raw_haiku)
    suffix_map_1 = map_word_to_word(corpus)
    suffix_map_2 = map_2_words_to_word(corpus)
    final = []

    choice = None
    while choice != "0":

        print(
            """
            Japanese Haiku Generator

            0 - Quit
            1 - Generate a full haiku
            2 - Regenerate Line 2
            3 - Regenerate Line 3
            """
            )

        choice = input("Choice: ")
        print()


        if choice == "0":
            sys.exit()
        elif choice == "1":
            final = []
            end_previous_line = []
            first_line, end_previous_line1 = haiku_line(suffix_order1, suffix_order2, word_list, end_previous_line, 5)
            final.append(first_line)
            line, end_previous_line2 = haiku_line(suffix_order1, suffix_order2,
                                              word_list, end_previous_line1, 7)
            final.append(line)
            line, end_prev_line3 = haiku_line(suffix_map_1, suffix_map_2,
                                              corpus, end_prev_line2, 5)
            final.append(line)
        elif choice == "2":
            if not final:
                print("Please generate a full haiku first (Option 1).")
                continue
            else:
                line, end_previous_line2 = haiku_line(suffix_order1, suffix_order2, word_list, end_previous_line1, 7)
                final[1] = line
        elif choice == "3":
            if not final:
                print("Please generate a full haiku first (Option 1).")
                continue
            else:
                line, end_previous_line3 = haiku_line(suffix_order1, suffix_order2, word_list, end_prev_line2, 5)
                final[2] = line
        else:
            print("\nSorry, but that isn't a valid choice.", file=sys.stderr)
            continue


        print()
        print("First line = ", end="")
        print(' '.join(final[0]), file=sys.stderr)
        print("Second line = ", end="")
        print(" ".join(final[1]), file=sys.stderr)
        print("Third line = ", end="")
        print(" ".join(final[2]), file=sys.stderr)
        print()

    input("\n\nPress the Enter key to exit.")

if __name__ == '__main__':
    main()
