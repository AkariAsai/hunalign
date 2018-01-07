import os
import subprocess
from tqdm import tqdm

en_file_list = os.listdir('/home/dl-exp/wiki_process/corpora_each/en')

for en_file in en_file_list:
    sys_call = "tail -n +3 " +en_file + " > " + en_file.split(".")[0] + "_removed.txt"
    subprocess.call(sys_call, shell=True)
    exit()
