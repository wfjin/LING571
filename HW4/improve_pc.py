import sys
import math
import nltk

def unique(list_of_prods):
    seen = set()
    return [x for x in list_of_prods if not (x in seen or seen.add(x))]

def add_rule_to_counter(productions, lhs_rhs_count, lhs_count, lhs, rhs):
    new_production = nltk.grammar.Production(lhs,rhs)
    productions.append(new_production)
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
    return

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
            productions_of_grammar.append(nltk.grammar.Production(lhs, rhs))
    add_rule_to_counter(productions_of_grammar, lhs_rhs_count, lhs_count, nltk.grammar.Nonterminal('NP_NNP'), ('Westchester',))
    add_rule_to_counter(productions_of_grammar, lhs_rhs_count, lhs_count, nltk.grammar.Nonterminal('CC'), ('either',))
    add_rule_to_counter(productions_of_grammar, lhs_rhs_count, lhs_count, nltk.grammar.Nonterminal('VBG'), ('Traveling',))
    add_rule_to_counter(productions_of_grammar, lhs_rhs_count, lhs_count, nltk.grammar.Nonterminal('IN'), ('during',))
    add_rule_to_counter(productions_of_grammar, lhs_rhs_count, lhs_count, nltk.grammar.Nonterminal('FRAG_VP'), (nltk.grammar.Nonterminal('VBG'),nltk.grammar.Nonterminal('NP')))
    add_rule_to_counter(productions_of_grammar, lhs_rhs_count, lhs_count, nltk.grammar.Nonterminal('NP_PRIME'), (nltk.grammar.Nonterminal('NP_PRIME'),nltk.grammar.Nonterminal('CC')))
    add_rule_to_counter(productions_of_grammar, lhs_rhs_count, lhs_count, nltk.grammar.Nonterminal('NP_PRIME'), (nltk.grammar.Nonterminal('CC'),nltk.grammar.Nonterminal('NNP')))

    new_prodcutions_of_grammar = unique(productions_of_grammar)
    
    output = open(sys.argv[2],'w')
    for production in new_prodcutions_of_grammar:
        lhs = production._lhs
        rhs = production._rhs
        prob = lhs_rhs_count[hash(lhs)][hash(rhs)]/lhs_count[hash(lhs)]  
        output.write(str(production)+' ['+str(prob)+']\n')

    