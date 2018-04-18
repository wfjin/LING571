import sys
import math
import nltk

class Pointer:
    def __init__(self, root, left, right, terminal):
        self._root = root
        self._left = left
        self._right = right
        self._terminal = terminal
        self._status = True
        if terminal == None:
            self._status = False   

    def root(self):
        return self._root

    def left(self):
        return self._left

    def right(self):
        return self._right

    def status(self):
        return self._status

    def terminal(self):
        return self._terminal

def cky(grammar, sentence):
    n = len(sentence)
    table = [[[] for i in range(n+1)] for j in range(n+1)]
    back_pointer = [[[] for i in range(n+1)] for j in range(n+1)]

    for j in range(1,n+1):
        for prod in grammar.productions():
            lhs = prod._lhs
            rhs = prod._rhs
            if sentence[j-1] in rhs:
                table[j-1][j].append(lhs)
                back_pointer[j-1][j].append(Pointer(lhs, None, None, sentence[j-1]))
        
        for i in reversed(range(0,j-1)):
            for k in range(i+1,j):
                for prod in grammar.productions():
                    lhs = prod._lhs
                    rhs = prod._rhs
                    if len(rhs) == 2:
                        B = rhs[0]
                        C = rhs[1]
                        if B in table[i][k] and C in table[k][j]:
                            table[i][j].append(lhs)
                            for b in back_pointer[i][k]:
                                for c in back_pointer[k][j]:
                                    if b.root() == B and c.root() == C:
                                        back_pointer[i][j].append(Pointer(lhs, b, c, None))
    return back_pointer[0][n]

def parse_tree_generate(back_pointer, start_symb, file_to_write, sent_length):
    num_parses = 0
    for ptr in back_pointer:
        if ptr.root() == start_symb:
            num_parses += 1
            file_to_write.write(str(parse_tree_generate_helper(ptr)))
            file_to_write.write('\n')
    return num_parses

def parse_tree_generate_helper(root_ptr):
    if root_ptr.status() == True:
        return nltk.tree.Tree(str(root_ptr.root()),[str(root_ptr.terminal())])
    else:
        left_subtree = parse_tree_generate_helper(root_ptr.left())
        right_subtree = parse_tree_generate_helper(root_ptr.right())
        return nltk.tree.Tree(str(root_ptr.root()), [left_subtree, right_subtree])

if __name__ == "__main__":
    grammar_file = sys.argv[1]
    grammar = nltk.data.load(grammar_file,'cfg')
    start_symb = grammar.start()
    sentences = list()
    sentences_toprint = list()
    file = open(sys.argv[2],'rU')
    for line in file:
        sentences_toprint.append(line)
        sentence = nltk.word_tokenize(line.strip())
        sentences.append(sentence)

    file_to_write = open(sys.argv[3],'w')
    for num in range(0,len(sentences)):
        file_to_write.write(sentences_toprint[num])
        back_pointer = cky(grammar, sentences[num])
        sent_length = len(sentences[num])
        num_parses = parse_tree_generate(back_pointer, start_symb, file_to_write, sent_length)
        file_to_write.write('Number of parses: '+str(num_parses)+'\n\n')