import sys
import csv
from tqdm import tqdm
from operator import itemgetter

result_files = ["align_result_0.txt", "align_result_100000.txt", \
                "align_result_200000.txt","align_result_300000.txt",\
                "align_result_400000.txt"]

score_dic = {}
pair_dic = {}

# load the result csv
index = 0
for result_file in result_files:
    with open(result_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            score_dic[index] = row[3]
            pair_dic[index] = (row[1], row[2])
            index+=1
        f.close()

print("The total number of aligned sentences : " + str(index))

result_f = open("sorted_alignment_result_weight_changed.csv", 'w')
writer = csv.writer(result_f, quoting=csv.QUOTE_NONNUMERIC)

for key, value in sorted(score_dic.items(), key=itemgetter(1), reverse = True):
    writer.writerow((pair_dic[key][0], pair_dic[key][1], score_dic[key]))

result_f.close()
