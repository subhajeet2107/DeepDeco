###################################################################
# This script creates vector dictionaries from the Glove 300d model
#
###################################################################

import pickle
import pandas as pd
import numpy as np
import csv
from argparse import ArgumentParser
import os

# arguments for this script
parser = ArgumentParser()

# Input
# text description of the furniture
parser.add_argument('--weight_path', type=str,
                    help='path to the pre-trained Word2Vec weight file',
                    metavar='IN_WT', required=False)

parser.add_argument('--input', type=str,
                    help='Input text description of the furniture',
                    metavar='IN_TEXT', required=False)

parser.add_argument('--content', type=str,
                    help='Input sketch image file including its file path',
                    metavar='IN_CONTENT', required=False)

words_weight = parser.parse_args()

# load pre-trained glove to words variable
if words_weight.weight_path is None:
    try:
        words_weight = pd.read_csv('src/stylesearch/pickles/glove.6B/glove.6B.300d.txt',
                        sep=" ",
                        index_col=0,
                        header=None,
                        quoting=csv.QUOTE_NONE)
    except FileNotFoundError:
        glove_file_path = (os.path.dirname(__file__)) + "/pickles/glove.6B/glove.6B.300d.txt"
        words_weight = pd.read_csv(glove_file_path, sep=" ", index_col=0, header=None, quoting=csv.QUOTE_NONE)


class Vectorizer:

    def __init__(self):
        print("Vectorizer loaded", self)

    # Vectorizer function
    def vec(self, word_string):
        """
        This function transforms a string into a 2D vector
        :param word_string: string
        :return: vector with shape(1, 300)
        """
        print('converting string {} into 2D vector shape(1, 300)'.format(word_string))
        flat_vec = words_weight.loc[word_string].values
        return flat_vec.reshape(1, 300)

    # sentence-to-vector conversion
    def sentence2vec(self, words_array):
        """
        This function transforms a 1D list of words from sentences into a 2D array of vector
        :param words_array: a 1D list of strings
        :return: a 2D array
        """
        running_sum = np.zeros((1, 300))
        for word in words_array:
            try:
                running_sum += self.vec(word)
            except Exception as e:
                print("This word does not exist in Glove.6B.300:{}.".format(word))
                continue
        return running_sum/len(words_weight)

    def text2img_mapping(self, img2text_dict):
        """
        This function creates a dictionary
        that has text vectors from image captions as keys
        and the corresponding image filename as values
        :param img2text_dict: image-to-text dictionary that has image file name as keys and image caption as values
        :return: a dictionary that has text vectors from image captions as keys
        and the corresponding image filename as values
        """
        for img_filename, desc_string in img2text_dict.items():
            words_array = desc_string.split(" ")
            print(words_array)
            print("current image file being processed", img_filename)
            sentence_vec = self.sentence2vec(words_array)
            text2img_dict[str(sentence_vec)] = img_filename
        return text2img_dict

    def img2vec_mapping(self, img2text_dict):
        """
        This function creates a dictionary
        that has image filename as keys
        and the corresponding text vectors from image captions as values
        :param img2text_dict: image-to-text dictionary that has image file name as keys and image caption as values
        :return: a dictionary that has image filename as keys
        and the corresponding text vectors from image captions as values
        """
        for img_filename, desc_string in img2text_dict.items():
            words_array = desc_string.split(" ")
            print(words_array)
            print("current image file being processed", img_filename)
            sentence_vec = self.sentence2vec(words_array)
            img2vec_dict[img_filename] = sentence_vec
        return img2vec_dict


# load img2text dictionary
try:
    img_to_text_pickle = open('src/stylesearch/pickles/img_to_text.p', 'rb')
except FileNotFoundError:
    img_to_text_pickle_file_path = (os.path.dirname(__file__)) + "/pickles/img_to_text.p"
    img_to_text_pickle = open(img_to_text_pickle_file_path, 'rb')

img2text_dict = pickle.load(img_to_text_pickle)
img_to_text_pickle.close()

# create a dictionary that has text vectors from image captions as keys and the corresponding image filename as values

# create a dictionary that has the furniture image file names as keys and
# the corresponding text vectors as values



