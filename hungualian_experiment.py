import sys
import subprocess

argvs = sys.argv
max_idx = argvs[1]

tmp_output_filename = 'align_tmp_' + str(max_idx) + '.txt'
result_filename = 'align_result_' + str(max_idx) + '.txt'
result_f = open(result_filename, 'w')

for i in range(10):
    ja_filename = '/home/dl-exp/wiki_process/corpora_each/ja/ja_' + str(i) + '.txt'
    en_filename = '/home/dl-exp/wiki_process/corpora_each/en/en_' + str(i) + '.txt'
    dic_filename = '/home/dl-exp/hunalign_akari/hunalign/data/en-ja-endict.txt'

    sys_call = 'src/hunalign/hunalign ' + dic_filename + ' ' + ja_filename + ' ' + \
        en_filename + ' -hand=examples/demo.manual.ladder -text >' + tmp_output_filename
    print(sys_call)

    subprocess.call(sys_call, shell=True)

    f = open(tmp_output_filename)
    line = f.readline()

    while line:
        result_f.write(line)
    f.close()

result_f.close()
