import nltk
import sys

if __name__ == "__main__":
    grammar_file = sys.argv[1]
    output = open(sys.argv[3],'w')
    grammar = nltk.data.load(grammar_file,'cfg')
    parser = nltk.parse.EarleyChartParser(grammar)
    sentences = []
    sentences_print = []
    with open(sys.argv[2],'r') as sentence_file:
        for line in sentence_file:
            sentences_print.append(line)
            sentence = nltk.word_tokenize(line)
            sentences.append(sentence)
    sent_num = len(sentences)
    parse_sum = 0
    for i in range(0,len(sentences)):
        sent = sentences[i]
        sent_print = sentences_print[i]
        output.write(sent_print)
        num_parses = 0
        for tree in parser.parse(sent):
            num_parses += 1
            output.write(str(tree))
            output.write('\n')
        parse_sum += num_parses
        output.write('Number of parses: '+str(num_parses))
        output.write('\n\n')
    output.write('Average parses per sentence: '+str(round((parse_sum/sent_num),3)))
    output.write('\n')