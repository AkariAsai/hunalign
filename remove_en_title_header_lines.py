import os
import subprocess
from tqdm import tqdm

en_file_list = os.listdir('/home/dl-exp/wiki_process/corpora_each/en')

for en_file in tqdm(en_file_list):
    full_en_file_name = '/home/dl-exp/wiki_process/corpora_each/en/' + en_file
    sys_call = "tail -n +3 " + full_en_file_name + " > " + full_en_file_name.split(".")[0]+ "_removed.txt"
    subprocess.call(sys_call, shell=True)
