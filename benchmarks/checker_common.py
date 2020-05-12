from enum import Enum

DEBUG = False
PRINT_LEN = 64


class Mode(Enum):
    Naive = 1
    Neighborhoods = 2


def log(str):
    if DEBUG:
        print(str)


def line_empty(line):
    return len(line.split('\t')) < 3


def get_query_filename_from_line(line):
    query = ''
    prevWord = ''
    for word in line.split(' '):
        if 'with' in prevWord:
            query = word
            break
        prevWord = word
    return query.split('/')[-1].strip('\n')


def get_query_class_from_line(line):
    query = ''
    prevWord = ''
    for word in line.split(' '):
        if 'with' in prevWord:
            query = word
            break
        prevWord = word
    return query.split('/')[-2].strip('\n')


def get_answer_filename_from_line(line):
    filename = line.split('\t')[-3]
    return filename.split('/')[-1].strip('\n')


def get_answer_class_from_line(line):
    filename = line.split('\t')[-3]
    return filename.split('/')[-2].strip('\n')


def get_FEI_from_line(line):
    score = line.split('\t')[-1].strip('\n')
    return float(score)
