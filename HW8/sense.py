from nltk.corpus import *
from nltk.corpus.reader.wordnet import information_content
import sys
import operator
import scipy

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

def read_ws(wsd):
    probe_word_list = list()
    noun_group_list = list()
    for line in wsd:
        words = (line.strip()).split('\t')
        if len(words) == 2:
            probe_word_list.append(words[0])
            noun_groups = words[1].split(',')
            noun_group_list.append(noun_groups)
    return probe_word_list, noun_group_list

def calc_sim(word, noun, wnic):
    word_syns = wordnet.synsets(word)
    noun_syns = wordnet.synsets(noun)
    sim_dict = dict()
    sim_decoder = dict()

    if noun_syns == []:
        return 0, 'NONSENSE'

    for word_s in word_syns:
        for noun_s in noun_syns:
            hash_id = hash((word_s, noun_s))
            sim_dict[hash_id] = 0
            sim_decoder[hash_id] = (word_s, noun_s)

    for word_s in word_syns:
        for noun_s in noun_syns:
            hash_id = hash((word_s, noun_s))
            subsumers = word_s.common_hypernyms(noun_s)    
            if len(subsumers) == 0:
                subsumer_ic = 0
            else:
                for sub in subsumers:
                    information_content(sub, wnic)
                subsumer_ic = max(information_content(s, wnic) for s in subsumers)
            sim_dict[hash_id] = subsumer_ic

    sorted_sims = sorted(sim_dict.items(), key=operator.itemgetter(1), reverse=True)
    max_pair = sorted_sims[0]
    hash_id = max_pair[0]
    (output_word_sense, output_noun) = sim_decoder[hash_id]
    return max_pair[1], output_word_sense.name()

def write_to_sys(probe_word_list, noun_group_list, wnic, output_file, words_to_output, sim_std):
    file_size = len(probe_word_list)
    for num in range(0, file_size):
        probe_word = probe_word_list[num]
        noun_groups = noun_group_list[num]
        senses = dict()
        for t in range(0, len(noun_groups)):
            noun = noun_groups[t]
            sim, word_sense = calc_sim(probe_word, noun, wnic)
            output_file.write('('+probe_word+', '+noun+', '+str(sim)+')')
            if t != len(noun_groups) - 1:
                output_file.write(' ')
            else:
                output_file.write('\n')
            if word_sense not in senses:
                senses[word_sense] = sim
            else:
                senses[word_sense] += sim
        sorted_senses = sorted(senses.items(), key=operator.itemgetter(1), reverse=True)
        pref_sense = sorted_senses[0][0]
        if pref_sense == 'NONSENSE':
            pref_sense = sorted_senses[1][0]
        output_file.write(pref_sense+'\n')

    pred_sim = list()
    for (word1, word2) in words_to_output:
        output_file.write(word1+','+word2+':')
        sim,_ = calc_sim(word1, word2, wnic)
        output_file.write(str(sim)+'\n')
        pred_sim.append(sim)
    correlation = scipy.stats.spearmanr(pred_sim, sim_std)
    output_file.write('Correlation:'+str(correlation[0])+'\n')

if __name__ == "__main__":
    if sys.argv[1] == 'nltk':
        wnic = wordnet_ic.ic('ic-brown-resnik-add1.dat')
    wsd_file = open(sys.argv[2], 'r')
    judgement_file = open(sys.argv[3], 'r')
    output_file = open(sys.argv[4], 'w')
    probe_word_list, noun_group_list = read_ws(wsd_file)
    word_to_output, sim_std = read_file(judgement_file)
    write_to_sys(probe_word_list, noun_group_list, wnic, output_file, word_to_output, sim_std)