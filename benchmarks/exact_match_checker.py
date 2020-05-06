import sys
import glob
from checker_common import *

TOP_N = 5
VERBOSE = False

def main():
    print()
    print('=' * PRINT_LEN)
    print('Calculating top-' + str(TOP_N) + ' accuracy')
    print('=' * PRINT_LEN)
    print()
    path = sys.argv[1] if len(sys.argv) > 1 else 'experiments/search_*_s2_f10_min2.txt'
    search_results = glob.glob(path)
    VERBOSE = True if (len(sys.argv) > 2 and sys.argv[2].upper() == "VERBOSE") else False
    all_results = { 'total_queries' : 0, 'total_naive_correct' : 0, 'total_neighborhoods_correct' : 0 }
    for file in search_results:
        parse_mode = Mode.Naive
        results = {
            'naive-correct-results' : 0, 'neighborhoods-correct-results' : 0,
            'naive-queries-count' : 0, 'neighborhoods-queries-count' : 0
        }
        result_counter = 0
        f = open(file, 'r')
        for line in f:
            if 'matched' in line:
                result_counter = 0
                query_filename = get_query_filename_from_line(line)
                log(query_filename)
                if 'neighborhoods' in line:
                    parse_mode = Mode.Neighborhoods
                    results['neighborhoods-queries-count'] += 1
                else:
                    parse_mode = Mode.Naive
                    results['naive-queries-count'] += 1
            else:
                if result_counter >= TOP_N or line_empty(line):
                    continue
                result_counter += 1
                answer_filename = get_answer_filename_from_line(line)
                log('\t' + answer_filename)
                if answer_filename == query_filename:
                    if parse_mode == Mode.Neighborhoods:
                        results['neighborhoods-correct-results'] += 1
                    else:
                        results['naive-correct-results'] += 1
        assert(results['naive-queries-count'] == results['neighborhoods-queries-count'])
        if VERBOSE:
            print('Class :', file)
            print('\tTotal queries            :', results['neighborhoods-queries-count'])
            print('\tAccuracy (naive)         :', round(results['naive-correct-results']/results['naive-queries-count'], 2) )
            print('\tAccuracy (neighborhoods) :', round(results['neighborhoods-correct-results']/results['neighborhoods-queries-count'], 2) )
            print()
        all_results['total_queries'] += results['naive-queries-count']
        all_results['total_naive_correct'] += results['naive-correct-results']
        all_results['total_neighborhoods_correct'] += results['neighborhoods-correct-results']
        f.close()
    print('=' * PRINT_LEN)
    print('Total queries                  :', all_results['total_queries'])
    print('Total accuracy (naive)         :', round(all_results['total_naive_correct']/all_results['total_queries'], 3))
    print('Total accuracy (neighborhoods) :', round(all_results['total_neighborhoods_correct']/all_results['total_queries'], 3))
    print('=' * PRINT_LEN)

main()
