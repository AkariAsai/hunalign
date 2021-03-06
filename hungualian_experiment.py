import sys
import subprocess
from tqdm import tqdm
import csv

argvs = sys.argv
start_idx = int(argvs[1])

tmp_output_filename = '20180212/align_tmp_' + str(start_idx) + '.txt'
result_filename = '20180212/align_' + str(start_idx) + '.txt'
result_f = open(result_filename, 'w')
writer = csv.writer(result_f, quoting=csv.QUOTE_NONNUMERIC)

for i in tqdm(range(start_idx, start_idx + 100000)):
    ja_filename = '/home/dl-exp/wiki_process/corpora_each/ja/ja_' + \
        str(i) + '.txt'
    en_filename = '/home/dl-exp/wiki_process/corpora_each/en/en_' + \
        str(i) + '_removed.txt'
    dic_filename = '/home/dl-exp/hunalign_akari/hunalign/data/en-ja-endict.txt'

    sys_call = 'src/hunalign/hunalign ' + dic_filename + ' ' + ja_filename + ' ' + \
        en_filename + ' -hand=examples/demo.manual.ladder -text >' + tmp_output_filename

    subprocess.call(sys_call, shell=True)

    f = open(tmp_output_filename, encoding='utf-8', errors='ignore')
    line = f.readline()

    # Add the result if the ja sentences could find the corresponding en
    # sentence.
    while line:
        result = line.split('\t')
        if len(result) >= 2 and len(result[0]) > 0 and float(result[2]) > -0.3:
            writer.writerow(
                (i, result[0], result[1], float(result[2])))
        line = f.readline()
    f.close()

result_f.close()
