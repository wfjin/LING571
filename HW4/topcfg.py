import sys
import math
import nltk

def unique(list_of_prods):
    seen = set()
    return [x for x in list_of_prods if not (x in seen or seen.add(x))]


if __name__ == "__main__":
    tree_bank = open(sys.argv[1],'r')
    productions_of_grammar = list()
    lhs_rhs_count = dict()
    lhs_count = dict()
    for parse_tree in tree_bank:
        t = nltk.tree.Tree.fromstring(parse_tree.strip())
        for production in t.productions():
            lhs = production._lhs
            rhs = production._rhs
            if hash(lhs) in lhs_rhs_count:
                lhs_count[hash(lhs)] += 1
                if hash(rhs) in lhs_rhs_count[hash(lhs)]:
                    lhs_rhs_count[hash(lhs)][hash(rhs)]+=1
                else:
                    lhs_rhs_count[hash(lhs)][hash(rhs)]=1
            else:
                lhs_count[hash(lhs)] = 1
                lhs_rhs_count[hash(lhs)]=dict()
                lhs_rhs_count[hash(lhs)][hash(rhs)]=1
        productions_of_grammar.extend(t.productions())
    new_prodcutions_of_grammar = unique(productions_of_grammar)
    
    output = open(sys.argv[2],'w')
    for production in new_prodcutions_of_grammar:
        lhs = production._lhs
        rhs = production._rhs
        prob = lhs_rhs_count[hash(lhs)][hash(rhs)]/lhs_count[hash(lhs)]
        output.write(str(production)+' ['+str(prob)+']\n')

    