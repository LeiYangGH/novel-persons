# -*- coding: utf-8 -*-
import jieba
import jieba.posseg as pseg

novel_file = '平凡的世界.txt'
family_names_file = '百家姓.txt'
output_names_file = '所有姓名.txt'


def read_file_lines(file):
    with open(file, 'r', encoding='utf8', errors='ignore') as f:
        return [l.strip() for l in f.readlines()]


def read_file(file):
    with open(file, 'r', encoding='utf8', errors='ignore') as f:
        return f.read()


def read_family_names(input_file):
    content = read_file(input_file)
    family_names = set([c for c in content if len(c.strip()) == 1])
    # print(family_names)
    return family_names


def extract_names(input_file):
    content = read_file(input_file)
    # jieba.enable_paddle()
    word_flag_list = list(pseg.cut(content, use_paddle=True))
    print(len(word_flag_list))
    distinct_word_flag_list = set(word_flag_list)
    print(len(distinct_word_flag_list))
    name_like_words = []
    for w, f in distinct_word_flag_list:
        if f in ['nr', 'PER']:
            name_like_words.append(w)
    return name_like_words


def write_names(names, file):
    with open(file, "w", encoding='utf-8') as fw:
        for n in names:
            fw.write(f'{n}\r\n')


if __name__ == '__main__':
    distinct_words = extract_names(novel_file)
    family_names = read_family_names(family_names_file)
    names = set([n for n in distinct_words
                 if (len(n) == 2 or len(n) == 3) and next((fn for fn in family_names if n.startswith(fn)), None)])
    print(rf'len(names)={len(names)}')
    print(names)
    write_names(names, output_names_file)
    print('end of main')
