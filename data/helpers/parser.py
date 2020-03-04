
import string
import re
import os
import pickle as pkl
from os import walk
#from bs4 import BeautifulSoup

import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

CONSTANTS_PATH = 'constants'

with open(CONSTANTS_PATH + '/ARABIC_LETTERS_LIST.pickle', 'rb') as file:
    ARABIC_LETTERS_LIST = pkl.load(file)

with open(CONSTANTS_PATH + '/DIACRITICS_LIST.pickle', 'rb') as file:
    DIACRITICS_LIST = pkl.load(file)

DN1 = 'clean-tashkeel'
DN2 = 'no-tashkeel'
DN3 = 'only-last-tashkeel'
DN4 = 'missing-last-tashkeel'

dir_path = '/Users/hassanfahmy/Documents/Stanford Classes/cs224n/project/cs224n-project/data/big-dataset/new-texts/كتب حديثة/كتب حديثة-original-'

files_paths = []
for (dir_path, dirs_names, files_names) in walk(dir_path):
    for file_name in files_names:
        files_paths.append(dir_path + os.sep + file_name)
print('Number of files:', len(files_paths))


def clean(file_path):
    print('Processing:', file_path)

    content = read_file_content(file_path)

    # content = remove_html_tags(content)
    # content = remove_urls(content)
    content = fix_diacritics(content)
    content = remove_english_letters(content)
    #content = remove_shift_j(content)
    content = fix_numbers(content)
    content = remove_white_spaces(content)
    without_diac_content = remove_diacritics(content)
    last_diac_content = remove_all_but_last_diacritic(content)
    no_last_diac_content = remove_last_diacritic(content)


    if len(content) == 0:
        return ''

    write_file_content(file_path, content, DN1)
    write_file_content(file_path, without_diac_content, DN2)
    write_file_content(file_path, last_diac_content, DN3)
    write_file_content(file_path, no_last_diac_content, DN4)
    # calculate_file_statistics(file_path, content, without_diac_content)

    return content


def read_file_content(file_path):
    return open(file_path).read()


def write_file_content(file_path, content, dir_name):
    file_path = file_path.split(os.sep)
    file_path = os.path.join(os.sep.join(file_path[:-1]), dir_name, file_path[-1])
    print('Writing:', file_path)
    with open(file_path, mode='w') as file_writer:
        file_writer.write(content)


def fix_diacritics(content):
    content = re.sub(r'اً', 'ًا', content)
    content = re.sub(r'(?P<char>[' + ''.join(ARABIC_LETTERS_LIST) + DIACRITICS_LIST[-1] + '])\s+(?P<diac>[' + ''.join(DIACRITICS_LIST) + ']+)(?P<brek>[\s+]|\Z)', r'\g<char>\g<diac>\g<brek>', content)
    content = re.sub(r'(?P<char>[^' + ''.join(ARABIC_LETTERS_LIST) + ''.join(DIACRITICS_LIST) + '])[' + ''.join(DIACRITICS_LIST) + ']+', r'\g<char>', content)
    content = re.sub(r'[' + DIACRITICS_LIST[-1] + ']+', DIACRITICS_LIST[-1], content)
    content = re.sub(r'(?P<diac>[' + ''.join(DIACRITICS_LIST[:-1]) + '])[' + ''.join(DIACRITICS_LIST) + ']+', r'\g<diac>', content)
    return content

def remove_english_letters(content):
    return ''.join([i for i in content if (i in ARABIC_LETTERS_LIST or i in DIACRITICS_LIST or i is ' ' or i.isdigit() )])
    #return content.translate(str.maketrans(string.ascii_letters, ' ' * len(string.ascii_letters)))



def fix_numbers(content):
    return re.sub(r'(?P<numb>[0-9]+)', r' \g<numb> ', content)


def remove_white_spaces(content):
    content = re.sub(r'[^\S\n]*\n[\s]*', '\n', content, flags=re.MULTILINE)
    content = re.sub(r'[^\S\n]+', ' ', content, flags=re.MULTILINE)
    content = re.sub(r'\A | \Z', '', content, flags=re.MULTILINE)
    return content

def remove_diacritics(content):
    return content.translate(str.maketrans('', '', ''.join(DIACRITICS_LIST)))


def remove_last_diacritic(content):
    string = ''
    for word in content.split(' '):
        if len(word) <= 1:
            print (""" error 
            last""")
            print (word)
        else:
            while word[-1] in DIACRITICS_LIST:
                word = word[:-1]
        word += ' '
        string += word
    return string



def remove_all_but_last_diacritic(content):
    string = ''
    for word in content.split(' '):
        i = -1
        if len(word) <= 1:
            print (""" error 
            but last""")
            print(word)
        else:
            while word[i] in DIACRITICS_LIST:
                i-=1
        word_suff = word[i:]
        word = remove_diacritics(word[:i])
        word = word + word_suff
        word += ' '
        string += word
    return string



os.mkdir(os.path.join(dir_path, DN1))
os.mkdir(os.path.join(dir_path, DN2))
os.mkdir(os.path.join(dir_path, DN3))
os.mkdir(os.path.join(dir_path, DN4))


for file_path in files_paths:
    clean(file_path)
print('Finished!')




