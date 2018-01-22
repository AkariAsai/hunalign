import sys
import csv
from tqdm import tqdm
from operator import itemgetter

result_files = ["align_result_weight_changed_0.txt", "align_result_weight_changed_100000.txt",
                "align_result_weight_changed_200000.txt", "align_result_weight_changed_300000.txt",
                "align_result_weight_changed_400000.txt"]

score_dic = {}
pair_dic = {}

# load the result csv
index = 0
for result_file in result_files:
    with open(result_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not len(row[1].split(' ')) / len(row[2].split(' ')) > 2.0:
                score_dic[index] = row[3]
                pair_dic[index] = (row[1], row[2])
                index += 1
        f.close()

print("The total number of aligned sentences : " + str(index))

result_f = open("sorted_alignment_result_weight_changed.csv", 'w')
result_ja_f = open("wiki_alignment_ja.txt", 'w')
result_en_f = open("wiki_alignment_en.txt", 'w')

writer = csv.writer(result_f, quoting=csv.QUOTE_NONNUMERIC)

for key, value in sorted(score_dic.items(), key=itemgetter(1), reverse=True):
    writer.writerow((key, pair_dic[key][0], pair_dic[key][1], score_dic[key]))
    result_ja_f.write(pair_dic[key][0] + '\n')
    result_en_f.write(pair_dic[key][1] + '\n')


result_f.close()
result_ja_f.close()
result_en_f.close()
