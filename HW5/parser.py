import nltk
import sys

if __name__ == "__main__":
    grammar_file = sys.argv[1]
    grammar = nltk.data.load(grammar_file)
    parser = nltk.parse.FeatureEarleyChartParser(grammar)
    output = open(sys.argv[3],'w')
    sentences = list()
    file = open(sys.argv[2],'rU')
    for line in file:
        sentence = nltk.word_tokenize(line.strip())
        sentences.append(sentence)
    for i in range(0,len(sentences)):
        sent = sentences[i]
        tree = parser.parse_one(sent)
        if tree != None:
            parse_string = ' '.join(str(tree).split()) 
            output.write(parse_string)
            output.write('\n')
        else:
            output.write('\n')    