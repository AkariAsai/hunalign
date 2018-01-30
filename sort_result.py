import sys
import csv
from tqdm import tqdm
from operator import itemgetter
import json
import csv

title2cat_filepath = "/home/dl-exp/wiki_process/category/result/title2category.json"
title2cat = json.load(open(title2cat_filepath, "r"))

corpas_info_filepath = "/home/dl-exp/wiki_process/corpora_idx_to_article_info.json"
corpas_info = json.load(open(corpas_info_filepath, "r"))


def get_categories_by_title(title):
    if title in title2cat:
        return title2cat[title]
    else:
        return None


def get_title_article_id_by_corpas_id(corpas_id):
    return get_title_by_corpas_id(corpas_id), \
        get_article_id_by_corpas_id(corpas_id)


def get_article_id_by_corpas_id(corpas_id):
    return corpas_info[str(corpas_id)]['article_index']


def get_title_by_corpas_id(corpas_id):
    return corpas_info[str(corpas_id)]["title"]


result_files = ["align_result_weight_changed_0.txt", "align_result_weight_changed_100000.txt",
                "align_result_weight_changed_200000.txt", "align_result_weight_changed_300000.txt",
                "align_result_weight_changed_400000.txt"]

score_dic = {}
pair_dic = {}
title_dic = {}
category_scores = {}

for result_file in result_files:
    with open(result_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not len(row[1].split(' ')) / len(row[2].split(' ')) > 2.0:
                corpas_id = \
                    int(row[0]) - int(result_file.lstrip("align_result_weight_changed_").rstrip(".txt"))
                title, article_id = \
                    get_title_article_id_by_corpas_id(corpas_id)

                # get scores for each categories
                categories = get_categories_by_title(title)
                print(title, row[0], categories)
                for category in categories:
                    category_scores.setdefault(category, [])
                    category_scores.append(float(row[3]))

                # Store enja_pair, score, title to dictionaries.
                score_dic[article_id] = row[3]
                pair_dic[article_id] = (row[1], row[2])
                title_dic[article_id]

                # TODO: remove this after debugging.
                print(title_dic)
                print(category_scores)
                exit()
        f.close()


print("The total number of aligned sentences : " + str(index))

result_f = open("sorted_alignment_result_weight_changed.csv", 'w')
result_ja_f = open("wiki_alignment_ja.txt", 'w')
result_en_f = open("wiki_alignment_en.txt", 'w')

writer = csv.writer(result_f, quoting=csv.QUOTE_NONNUMERIC)

for key, value in sorted(score_dic.items(), key=itemgetter(1), reverse=True):
    writer.writerow((title[key], pair_dic[key][0],
                     pair_dic[key][1], score_dic[key]))
    result_ja_f.write(pair_dic[key][0] + '\n')
    result_en_f.write(pair_dic[key][1] + '\n')


result_f.close()
result_ja_f.close()
result_en_f.close()
