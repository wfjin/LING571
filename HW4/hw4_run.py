import os
import sys

if __name__ == "__main__":

    treebank_filename = sys.argv[1]
    output_pcfg_file = sys.argv[2]
    test_sentence = sys.argv[3]
    baseline_output = sys.argv[4]
    input_pcfg_file = sys.argv[5]
    improved_output = sys.argv[6]
    base_eval = sys.argv[7]
    improved_eval = sys.argv[8]

    os.system('python3 topcfg.py '+treebank_filename+' '+output_pcfg_file)
    os.system('python3 parser.py '+output_pcfg_file+' '+test_sentence+' '+baseline_output)
    os.system('python3 improve_pc.py '+treebank_filename+' '+input_pcfg_file)
    os.system('python3 improve.py '+input_pcfg_file+' '+test_sentence+' '+improved_output)
    os.system('/dropbox/17-18/571/hw4/tools/evalb -p /dropbox/17-18/571/hw4/tools/COLLINS.prm /dropbox/17-18/571/hw4/data/parses.gold '+baseline_output+' > '+base_eval)
    os.system('/dropbox/17-18/571/hw4/tools/evalb -p /dropbox/17-18/571/hw4/tools/COLLINS.prm /dropbox/17-18/571/hw4/data/parses.gold '+improved_output+' > '+improved_eval)