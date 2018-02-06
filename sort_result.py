import sys
import csv
from tqdm import tqdm
from operator import itemgetter

corpora_idx_to_article_info = \
    json.load(open("/home/dl-exp/wiki_process/corpora_idx_to_article_info.json", "r"))
title2category = \
    json.load(open("/home/dl-exp/wiki_process/category/result/title2category.json", "r"))

def get_title_article_id_by_corpora_id(corpora_id):
    return corpora_idx_to_article_info[corpora_id]['title'], \
            corpora_idx_to_article_info[corpora_id]['article_index']

def get_categories_title_by_article_title(title):
    if title in title2category.keys():
        categories = title2category[title]
        return categories
    else:
        return None

def get_categories_by_corpora_id(corpora_id):
    title = corpora_idx_to_article_info[corpora_id]['title']
    return get_categories_title_by_article_title(title)


def create_category_score_dic(score_dic, article_title):
    for k, v in score_dic.items():
        categories = get_categories_title_by_article_title(article_title[k])
        




result_files = ["align_result_weight_changed_0.txt", "align_result_weight_changed_100000.txt",
                "align_result_weight_changed_200000.txt", "align_result_weight_changed_300000.txt",
                "align_result_weight_changed_400000.txt"]

score_dic = {}
pair_dic = {}
article_title = {}

# load the result csv
for result_file in result_files:
    with open(result_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not len(row[1].split(' ')) / len(row[2].split(' ')) > 2.0:
                corpora_id = int(row[0]) - int(result_file.lstrip('align_result_weight_changed_').rstrip('.txt'))
                title, article_id = get_title_article_id_by_corpora_id(corpora_id)

                article_title[article_id] = title
                score_dic[article_id] = row[3]
                pair_dic[article_id] = (row[1], row[2])

        f.close()

print("The total number of aligned sentences : " + str(index))

result_f = open("sorted_alignment_result_weight_changed.csv", 'w')
result_ja_f = open("wiki_alignment_ja.txt", 'w')
result_en_f = open("wiki_alignment_en.txt", 'w')

writer = csv.writer(result_f, quoting=csv.QUOTE_NONNUMERIC)

for key, value in sorted(score_dic.items(), key=itemgetter(1), reverse=True):
    title = article_title[key]
    writer.writerow((title, pair_dic[key][0], pair_dic[key][1], score_dic[key]))
    result_ja_f.write(pair_dic[key][0] + '\n')
    result_en_f.write(pair_dic[key][1] + '\n')



result_f.close()
result_ja_f.close()
result_en_f.close()
