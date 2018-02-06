# This is a script to run a experiment which aims at comparing the perfomance of
# hunalign with different params and the use of cognate score.
import sys
import subprocess
from tqdm import tqdm
import csv
import random


def create_randomly_sampled_en(en_filepath):
    en_f = open(en_filepath, "r")
    en_f_sampled_filepath = en_filepath.split(".en")[0] + "_sampled.en"
    en_f_sampled = open(en_f_sampled_filepath, "w")

    line = en_f.readline()
    while line:
        if random.randint(0, 3) % 2 != 0:
            en_f_sampled.write(line + "\n")
        line = en_f.readline()

    en_f.close()
    en_f_sampled.close()

    return en_f_sampled_filepath


kyoto_wiki_ja_filepath = "/home/dl-exp/data/kyoto_wiki/kyoto_wiki_HST_100.ja"
kyoto_wiki_en_filepath = "/home/dl-exp/data/kyoto_wiki/kyoto_wiki_HST_100.en"

kyoto_wiki_en_filepath_sampled = \
    create_randomly_sampled_en(kyoto_wiki_en_filepath)

tmp_filename = 'align_improvement_exp_tmp.txt'

dic_filename = '/home/dl-exp/hunalign_akari/hunalign/data/en-ja-endict.txt'

sys_call = 'src/hunalign/hunalign ' + dic_filename + ' ' + kyoto_wiki_ja_filepath + ' ' + \
    kyoto_wiki_en_filepath_sampled + \
    ' -hand=examples/demo.manual.ladder -text >' + tmp_filename

subprocess.call(sys_call, shell=True)

f = open(tmp_filename)
line = f.readline()

result_filename = 'align_improvement_exp.txt'
result_f = open(result_filename, 'w')
writer = csv.writer(result_f, quoting=csv.QUOTE_NONNUMERIC)

while line:
    result = line.split('\t')
    if len(result[0]) > 0 and float(result[2]) > -0.3:
        writer.writerow(
            (i, result[0], result[1], float(result[2])))
    line = f.readline()
f.close()

result_f.close()
