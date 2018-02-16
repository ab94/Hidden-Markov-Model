import sys
import json

" Learn the emission and transition probabilities from the tagged data set "

""" Accept input file and store it in a dict """


def parse_input():
    input_file = sys.argv[1]
    if input_file is None:
        print("ERROR: Enter a file name for training data")

    file = open(input_file, "r", encoding='utf-8')

    word_to_tagdict = {}
    total_tag_count = {}
    last_word_count = {}
    tag_transition = {}

    for line in file:
        word_list = line.split(" ")
        for index, word_with_tag in enumerate(word_list):
            word = get_word(word_with_tag)
            tag = get_tag(word_with_tag)

            # remove the newline character from last word of each line.
            if index == len(word_list) - 1:
                tag = tag[:-1]

            calculate_emission_terms(total_tag_count, tag, word_to_tagdict, word)
            calculate_transition_terms(tag_transition, word_list, tag, index, last_word_count)

    print(last_word_count)
    print(tag_transition)
    print(word_to_tagdict)
    print(total_tag_count)
    output = {
        "tag_transitions": tag_transition,
        "emission": word_to_tagdict,
    }
    output_file = open("hmmmodel.txt", 'w')
    json.dump(output, output_file)


def calculate_transition_terms(tag_transition, word_list, tag, index, last_word_count):
    if index is 0:
        if "start" not in tag_transition:
            tag_transition["start"] = {}
        dictionary = tag_transition["start"]
        add_one(dictionary, tag)

    if tag not in tag_transition:
        tag_transition[tag] = {}
    dictionary = tag_transition[tag]

    if index != len(word_list) - 1:
        add_one(dictionary, get_tag(word_list[index + 1]))
    else:
        add_one(dictionary, "end")
        add_one(last_word_count, tag)


def calculate_emission_terms(total_tag_count, tag, word_to_tagdict, word):
    add_one(total_tag_count, tag)

    # check if word exists in the dictionary
    if word not in word_to_tagdict:
        word_to_tagdict[word] = {}

    dictionary = word_to_tagdict[word]
    add_one(dictionary, tag)



def add_one(dictionary, key):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1


def find_last_slash(word):
    # Iterate the word from last to first character.
    index = len(word)
    for char in word[::-1]:
        if char == '/':
            return index
        index -= 1


def get_tag(word_with_tag):
    last_slash_index = find_last_slash(word_with_tag)
    tag = word_with_tag[last_slash_index:]

    return tag


def get_word(word_with_tag):
    last_slash_index = find_last_slash(word_with_tag)
    word = word_with_tag[:last_slash_index - 1]
    return word


if __name__ == "__main__":
    parse_input()

