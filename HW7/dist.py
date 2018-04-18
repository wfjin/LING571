import nltk
import sys
import string
import operator
import numpy as np
import scipy
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

def process_word(brown_words):
    new_list = list()
    for word in brown_words:
        if re.match("^\W+$",word):
            continue
        else:
            new_list.append(word.lower())
    return new_list

def remove_duplicates(li):
    my_set = set()
    res = []
    for e in li:
        if e not in my_set:
            res.append(e)
            my_set.add(e)
    return res

def create_neighbor(brown_sents, window):
    new_list_of_neighbors = list()
    for sent in brown_sents:
        sent_size = len(sent)
        for num in range(0, sent_size):
            word_neighbor = list()
            if num-window < 0:
                for n in range(0, num):
                    word_neighbor.append(sent[n])
                if num+window < sent_size-1:
                    for m in range(num+1, num+window+1):
                        word_neighbor.append(sent[m])
                else:
                    for m in range(num+1, sent_size):
                        word_neighbor.append(sent[m])
                new_list_of_neighbors.append(word_neighbor)
                continue
            elif num+window > sent_size-1:
                for q in range(num+1, sent_size):
                    word_neighbor.append(sent[q])
                if num-window >= 0:
                    for p in range(num-window,num):
                        word_neighbor.append(sent[p])
                else:
                    for p in range(0,num):
                        word_neighbor.append(sent[p])
                new_list_of_neighbors.append(word_neighbor)
                continue
            else:
                for k in range(num-window, num):
                    word_neighbor.append(sent[k])
                for l in range(num+1, num+window+1):
                    word_neighbor.append(sent[l])
                new_list_of_neighbors.append(word_neighbor)
    return new_list_of_neighbors

def calc_counts(brown_words, neighborhood):
    neighbors_no_dups = dict()
    word_no_dups = remove_duplicates(brown_words)
    for num in range(0, len(brown_words)):
        hash_id = hash(brown_words[num])
        if hash_id not in neighbors_no_dups:
            neighbors_no_dups[hash_id] = dict()
        for word in neighborhood[num]:
            if word not in neighbors_no_dups[hash_id]:
                neighbors_no_dups[hash_id][word] = 1
            else:
                neighbors_no_dups[hash_id][word] += 1
    return neighbors_no_dups

def find_all_feats(counts):
    feat_set = set()
    for hash_id in counts:
        for feat in counts[hash_id]:
            feat_set.add(feat)
    return feat_set

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

def calc_sim(word_1, word_2, feat_vecs, brown_words):
    feature_vector_1 = feat_vecs[hash(word_1)]
    feature_vector_2 = feat_vecs[hash(word_2)]
    sorted_vector_1 = sorted(feature_vector_1.items(), key=operator.itemgetter(1), reverse=True)
    sorted_vector_2 = sorted(feature_vector_2.items(), key=operator.itemgetter(1), reverse=True)
    list_of_feats = list()
    for feat in feature_vector_1:
        if feat not in list_of_feats:
            list_of_feats.append(feat)
    for feat in feature_vector_2:
        if feat not in list_of_feats:
            list_of_feats.append(feat)

    matrix_1 = np.zeros(len(list_of_feats))
    matrix_2 = np.zeros(len(list_of_feats))

    for num in range(0, len(list_of_feats)):
        if list_of_feats[num] in feature_vector_1:
            matrix_1[num] = feature_vector_1[list_of_feats[num]]
        else:
            matrix_1[num] = 0
        if list_of_feats[num] in feature_vector_2:
            matrix_2[num] = feature_vector_2[list_of_feats[num]]
        else:
            matrix_2[num] = 0
    cos_sim = 1-scipy.spatial.distance.cosine(matrix_1, matrix_2)

    if len(sorted_vector_1) >= 10 and len(sorted_vector_1) >= 10:
        return cos_sim, sorted_vector_1[0:10], sorted_vector_2[0:10]
    elif len(sorted_vector_1) >= 10 and len(sorted_vector_1) < 10:
        return cos_sim, sorted_vector_1[0:10], sorted_vector_2
    elif len(sorted_vector_1) < 10 and len(sorted_vector_1) >= 10:
        return cos_sim, sorted_vector_1, sorted_vector_2[0:10]
    else:
        return cos_sim, sorted_vector_1, sorted_vector_2

def write_to_sys(sys_file, word_to_sys, feat_vec, brown_words):
    list_of_sim = list()
    for word_pair in word_to_sys:
        word_1 = word_pair[0]
        word_2 = word_pair[1]
        cos_sim, features_1, features_2 = calc_sim(word_1, word_2, feat_vec, brown_words)
        sys_file.write(word_1+': ')
        for pair in features_1:
            sys_file.write(pair[0]+':'+str(pair[1])+' ')
        sys_file.write('\n')
        sys_file.write(word_2+': ')
        for pair in features_2:
            sys_file.write(pair[0]+':'+str(pair[1])+' ')
        sys_file.write('\n')
        sys_file.write(word_1+','+word_2+':'+str(cos_sim)+'\n')
        list_of_sim.append(cos_sim)
    return list_of_sim

def store_all_feature_counts(counts):
    feature_counts = dict()
    for hash_id in counts:
        for word in counts[hash_id]:
            if word not in feature_counts:
                feature_counts[hash(word)] = counts[hash_id][word]
            else:
                feature_counts[hash(word)] += counts[hash_id][word]
    return feature_counts

def calc_prob(counts, word_to_sys, brown_words):
    neighbors_pmi = dict()
    feature_counts = store_all_feature_counts(counts)
    corpus_size = len(brown_words)
    for pair in word_to_sys:
        for elem in pair:
            hash_id = hash(elem)
            neighbors_pmi[hash_id] = dict()
            p_i = brown_words.count(elem)
            for word in counts[hash_id]:
                p_ij = counts[hash_id][word]
                p_j = brown_words.count(word)
                neighbors_pmi[hash_id][word] = max(np.log2((corpus_size*p_ij)/(p_i*p_j)),0)
    return neighbors_pmi
    
if __name__ == "__main__":
    brown_sents = list(nltk.corpus.brown.sents())
    process_sents = process_word_list(brown_sents)

    brown_words = list(nltk.corpus.brown.words())
    process_words = process_word(brown_words)
    window_size = int(sys.argv[1])
    weighting = sys.argv[2]
    judgement = open(sys.argv[3], 'r')
    sys_file = open(sys.argv[4], 'w')
    word_to_sys, sim_std = read_file(judgement)
    
    neighborhood = create_neighbor(process_sents, window_size)

    counts = calc_counts(process_words, neighborhood)

    if weighting == 'FREQ':
        list_of_sim = write_to_sys(sys_file, word_to_sys, counts, process_words)
        correlation = scipy.stats.spearmanr(list_of_sim, sim_std)
        sys_file.write('Correlation:'+str(correlation[0])+'\n')
    elif weighting == 'PMI':
        PMIs = calc_prob(counts, word_to_sys, process_words)
        list_of_sim_2 = write_to_sys(sys_file, word_to_sys, PMIs, process_words)
        correlation_2 = scipy.stats.spearmanr(list_of_sim_2, sim_std)
        sys_file.write('Correlation:'+str(correlation_2[0])+'\n')


    
