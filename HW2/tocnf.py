import nltk
import sys

def unit_conversion_loop(productions, lhs, rhs):
    new_prod_list = list()
    for grammar_rule in productions:
        lhs_2 = grammar_rule._lhs
        rhs_2 = grammar_rule._rhs
        if rhs[0] == lhs_2 and len(rhs_2) == 1:
            new_rhs = (rhs_2[0],)
            new_prod = nltk.grammar.Production(lhs,new_rhs)
            new_prod_list.append(new_prod)
        elif rhs[0] == lhs_2 and len(rhs_2) != 1:
            new_rhs = rhs_2
            new_prod = nltk.grammar.Production(lhs,new_rhs)
            new_prod_list.append(new_prod)
        else:
            continue
    return new_prod_list

def unit_conversion_loop_list(productions, rule_list):
    output_list = list()
    for rule in rule_list:
        lhs = rule._lhs
        rhs = rule._rhs
        if len(rhs) != 1 or nltk.grammar.is_terminal(rhs[0]):
            output_list.append(rule)
        else:
            new_list = unit_conversion_loop(productions, lhs, rhs)
            if len(new_list) != 0:
                output_list.extend(unit_conversion_loop_list(productions, new_list))
    return output_list                

def list_replace(target_list, symb1, symb2):
    out_list = list()
    for symb in target_list:
        if symb == symb1:
            out_list.append(symb2)
        else:
            out_list.append(symb1)
    return out_list

if __name__ == "__main__":
    grammar_file = sys.argv[1]
    output = open(sys.argv[2],'w')
    grammar = nltk.data.load(grammar_file,'cfg')
    start_symb = grammar.start()
    new_productions = list()
    for grammar_rule in grammar.productions():
        lhs = grammar_rule._lhs
        rhs = grammar_rule._rhs
        if nltk.grammar.is_nonterminal(lhs) and len(rhs) == 1:
            new_productions.append(grammar_rule)
        else:
            new_nonterm_to_term_rule_list = list()
            new_rhs = tuple()
            for symb in rhs:
                if nltk.grammar.is_terminal(symb):
                    new_repl_lhs = nltk.grammar.Nonterminal(str(symb)+"_TERM")
                    new_repl_rhs = (symb,)
                    new_repl_prod = nltk.grammar.Production(new_repl_lhs,new_repl_rhs)
                    new_nonterm_to_term_rule_list.append(new_repl_prod)
                    new_rhs = new_rhs + (new_repl_lhs,)
                else:
                    new_rhs = new_rhs + (symb,)
            new_rule = nltk.grammar.Production(lhs,new_rhs)
            new_productions.append(new_rule)
            for rule in new_nonterm_to_term_rule_list:
                new_productions.append(rule)

    new_productions_2 = list()
    for grammar_rule in new_productions:
        lhs = grammar_rule._lhs
        rhs = grammar_rule._rhs
        if nltk.grammar.is_nonterminal(lhs) and len(rhs) != 1:
            new_productions_2.append(grammar_rule)
        elif nltk.grammar.is_nonterminal(lhs) and len(rhs) == 1 and nltk.grammar.is_terminal(rhs[0]):
            new_productions_2.append(grammar_rule)
        else:
            new_rule_list = unit_conversion_loop(new_productions,lhs,rhs)
            try:
                out_list = unit_conversion_loop_list(new_productions, new_rule_list)
            except:
                print('Error: this is a dead-end rule')
            for rule in out_list:
                new_productions_2.append(rule)

    new_productions_3 = list()
    for grammar_rule in new_productions_2:
        lhs = grammar_rule._lhs
        rhs = grammar_rule._rhs
        if nltk.grammar.is_nonterminal(lhs) and len(rhs) <= 2:
            new_productions_3.append(grammar_rule)
        else:
            new_main_rhs = list(rhs)
            new_rule_list = list()
            while len(new_main_rhs)>2:
                new_lhs = nltk.grammar.Nonterminal(str(new_main_rhs[0])+"-"+str(new_main_rhs[1]))
                new_rhs = (new_main_rhs[0],new_main_rhs[1])
                new_main_rhs.pop(0)
                new_main_rhs.pop(0)
                new_main_rhs.insert(0,new_lhs)
                new_prod = nltk.grammar.Production(new_lhs,new_rhs)
                new_rule_list.append(new_prod)
            new_main_prod = nltk.grammar.Production(lhs,new_main_rhs)
            new_productions_3.append(new_main_prod)
            for rule in new_rule_list:
                new_productions_3.append(rule)
    new_grammar = nltk.grammar.CFG(start_symb, new_productions_3)
    #print(new_grammar.is_chomsky_normal_form())
    output.write(str('%start ')+str(start_symb)+'\n')
    prod_set = set()
    for prod in new_grammar.productions():
        prod_set.add(prod)
    for prod in prod_set:
        output.write(str(prod)+'\n')

            






    



