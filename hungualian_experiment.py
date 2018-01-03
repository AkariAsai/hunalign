import sys
import subprocess
from tqdm import tqdm

argvs = sys.argv
start_idx = int(argvs[1])

tmp_output_filename = 'align_tmp_' + str(start_idx) + '.txt'
result_filename = 'align_result_' + str(start_idx) + '.txt'
result_f = open(result_filename, 'w')

for i in tqdm(range(start_idx, start_idx+10000)):
    ja_filename = '/home/dl-exp/wiki_process/corpora_each/ja/ja_' + str(i) + '.txt'
    en_filename = '/home/dl-exp/wiki_process/corpora_each/en/en_' + str(i) + '.txt'
    dic_filename = '/home/dl-exp/hunalign_akari/hunalign/data/en-ja-endict.txt'

    sys_call = 'src/hunalign/hunalign ' + dic_filename + ' ' + ja_filename + ' ' + \
        en_filename + ' -hand=examples/demo.manual.ladder -text >' + tmp_output_filename

    subprocess.call(sys_call, shell=True)

    f = open(tmp_output_filename)
    line = f.readline()

    # Add the result if the ja sentences could find the corresponding en sentence.
    while line:
        result = line.split('\t')
        if len(result[0]) > 0 and float(result[2]) > -0.3:
            result_f.write(result[0] +','+ result[1] + ',' + result[2])
        line = f.readline()
    f.close()

result_f.close()
