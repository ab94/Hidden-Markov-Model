import sys
import json

model_parameters_path = "hmmmodel.txt"
output_file_path = "hmmoutput.txt"


def decode():

    input_file = sys.argv[1]
    if input_file is None:
        print("ERROR: Enter path to input file to tag.")
        exit(1)

    input_file = open(input_file, "r", encoding='utf-8')
    get_model_parameters()
    decode_from_file(input_file)


def decode_from_file(input_file):
    output_file = open(output_file_path, 'w', encoding='utf-8')

    for line in input_file:
        word_list = line.split(" ")
        word_prob = {}
        backpointer = {}
        calculate_word_probability(word_list, word_prob, backpointer)

        tag = get_backpointers(word_prob, backpointer, word_list)
        write_output(output_file, word_list, tag)


def calculate_word_probability(word_list, word_prob, backpointer):
    for index, word in enumerate(word_list):
        if index == len(word_list) - 1:
            word = word[:-1]

        calculate_prob(word, index, word_list, word_prob, backpointer)


def calculate_prob(word, index, word_list, word_prob, backpointer):
        # New word; Never occured in training set.
        if word not in emission:
            tag_dict = add_all_tags_to_dict()
        else:
            tag_dict = emission[word]
        for tag, frequency in tag_dict.items():
            # emission_probability = 1 for new words(frequency = 0) so that the term is ignored in total probability calculations.
            if frequency == 0:
                emission_prob = 1
            else:
                emission_prob = frequency / total_tag_count[tag]
            if index not in word_prob:
                word_prob[index] = {}
                backpointer[index] = {}
            word_prob[index][tag] = 0
            # TRANSITION PROBABILITY
            calculate_transition_probability(tag, index, word_list, emission_prob, word_prob, backpointer)


# calculate the transition probabilities for the current word/TAG from all tags for the previous word,
# store the highest probability tag as the backpointer for this word/TAG.
def calculate_transition_probability(tag, index, word_list, emission_prob, word_prob, backpointer):
            if index == 0:
                dictionary = tag_transition["start"]
                if tag in dictionary:
                    transition_prob = dictionary[tag] / line_count
                    word_prob[index][tag] = emission_prob * transition_prob
                else:
                    word_prob[index][tag] = 0
            else:
                prev_word = word_list[index - 1]
                # for every tag in previous word, calculate the transition prob
                for prev_tag, prev_prob in word_prob[index - 1].items():
                    if tag not in tag_transition[prev_tag]:
                        continue
                    if prev_tag not in last_word_count:
                        last_tag_count = 0
                    else:
                        last_tag_count = last_word_count[prev_tag]
                    transition_prob = (tag_transition[prev_tag][tag] / (total_tag_count[prev_tag] - last_tag_count))
                    new_prob = prev_prob * transition_prob * emission_prob
                    if new_prob > word_prob[index][tag]:
                        word_prob[index][tag] = new_prob
                        backpointer[index][tag] = prev_tag


# construct the backpointers from the calculated probabilities.
def get_backpointers(word_prob, backpointer, word_list):
        max_value = 0
        max_tag = ""
        for tag, value in word_prob[len(word_list) - 1].items():
            if value > max_value:
                max_value = value
                max_tag = tag
        tag = {}
        for index in range(len(word_list) - 1, -1, -1):
            tag[index] = max_tag
            if max_tag in backpointer[index]:
                max_tag = backpointer[index][max_tag]
        return tag


# output the word/TAG values to the output file.
def write_output(output_file, word_list, tag):
    for index in range(0, len(word_list)):
        if index == len(word_list) - 1:
            word_list[index] = word_list[index][:-1]
        print("%s/%s " % (word_list[index], tag[index]), end="")
        # dump output to output file
        output_file.write("%s/%s" % (word_list[index], tag[index]))
        if index != (len(word_list) - 1):
            output_file.write(" ")
    print()
    output_file.write("\n")


def get_model_parameters():
    model = json.load(open(model_parameters_path, encoding='utf-8'))
    global total_tag_count, emission, last_word_count, tag_transition, line_count
    total_tag_count = model["total_tag_count"]
    emission = model["emission"]
    last_word_count = model["last_word_count"]
    tag_transition = model["tag_transitions"]
    line_count = model["line_count"]


def add_all_tags_to_dict():
    all_tags = {}
    for tag, value in total_tag_count.items():
        all_tags[tag] = 0
    return all_tags



if __name__ == "__main__":
    decode()