import nltk
import sys
import string
import operator
import numpy as np
import scipy
import gensim
import re

def process_word_list(brown_sents):
    new_list = list()
    for sent in brown_sents:
        sent_list = list()
        for word in sent:
            if re.match("^\W+$",word):
                continue
            else:
                sent_list.append(word.lower())
        new_list.append(sent_list)
    return new_list

def read_file(judge):
    words_to_output = list()
    sim_std = list()
    for line in judge:
        words = (line.strip()).split(',')
        if len(words) == 3:
            pair = (words[0],words[1])
            words_to_output.append(pair)
            sim_std.append(float(words[2]))
    return words_to_output, sim_std

def write_to_sys(sys_file, word_to_sys, model):
    list_of_sim = list()
    for word_pair in word_to_sys:
        word_1 = word_pair[0]
        word_2 = word_pair[1]
        sim = model.similarity(word_1, word_2)
        sys_file.write(word_1+','+word_2+':'+str(sim)+'\n')
        list_of_sim.append(sim)
    return list_of_sim
    
if __name__ == "__main__":
    brown_sents = list(nltk.corpus.brown.sents())
    process_sents = process_word_list(brown_sents)
    window_size = int(sys.argv[1])
    judgement = open(sys.argv[2], 'r')
    sys_file = open(sys.argv[3], 'w')
    model = gensim.models.Word2Vec(process_sents, size=100, window=window_size, min_count=1, workers=1)
    word_to_output, sim_std = read_file(judgement)
    list_of_sim = write_to_sys(sys_file, word_to_output, model)
    correlation = scipy.stats.spearmanr(list_of_sim, sim_std)
    sys_file.write('Correlation:'+str(correlation[0])+'\n')

