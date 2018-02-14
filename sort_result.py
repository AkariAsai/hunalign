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


corpora_idx_to_article_info = \
    json.load(
        open("/home/dl-exp/wiki_process/corpora_idx_to_article_info.json", "r"))
title2category = \
    json.load(
        open("/home/dl-exp/wiki_process/category/result/title2category.json", "r"))


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


result_files = ["20180212/align_0.txt", "20180212/align_100000.txt",
                "20180212/align_200000.txt", "20180212/align_300000.txt",
                "20180212/align_400000.txt"]

score_dic = {}
pair_dic = {}
title_dic = {}

index = 0
for result_file in result_files:
    with open(result_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not len(row[1].split(' ')) / len(row[2].split(' ')) > 2.0:
                corpas_id = int(row[0]) - (100000 * index)
                title, article_id = \
                    get_title_article_id_by_corpas_id(corpas_id)

                # get scores for each categories
                categories = get_categories_by_title(title)
                if categories is not None:
                    for category in categories:
                        category_scores.setdefault(category, [])
                        category_scores[category].append(float(row[3]))

                # Store enja_pair, score, title to dictionaries.
                score_dic[article_id] = row[3]
                pair_dic[article_id] = (row[1], row[2])
                title_dic[article_id] = title
                count += 1
        f.close()
    index += 1


with open('20180212/category_score.json', 'w') as fp:
    json.dump(category_scores, fp)

print("The total number of aligned sentences : " + str(count))

result_f = open("20180212/sorted_alignment_title_info.csv", 'w')
result_ja_f = open("20180212/wiki_alignment_ja.txt", 'w')
result_en_f = open("20180212/wiki_alignment_en.txt", 'w')

writer = csv.writer(result_f, quoting=csv.QUOTE_NONNUMERIC)

for key, value in sorted(score_dic.items(), key=itemgetter(1), reverse=True):
    title = title_dic[key]
    writer.writerow(
        (title, pair_dic[key][0], pair_dic[key][1], score_dic[key]))
    result_ja_f.write(pair_dic[key][0] + '\n')
    result_en_f.write(pair_dic[key][1] + '\n')


result_f.close()
result_ja_f.close()
result_en_f.close()
