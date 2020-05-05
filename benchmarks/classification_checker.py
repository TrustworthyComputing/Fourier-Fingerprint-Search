import glob
from checker_common import *

TOP_N = 5

def main():
    print()
    print('=' * PRINT_LEN)
    print('Calculating classification accuracy based on first ' + str(TOP_N) + ' results')
    print('=' * PRINT_LEN)
    print()
    search_results = glob.glob("benchmarks_search/search_*_s2_f10.txt")
    all_results = { 'total_queries' : 0, 'total_naive_correct' : 0, 'total_neighborhoods_correct' : 0 }
    for file in search_results:
        parse_mode = Mode.Naive
        results = {
            'naive-correct-results' : 0, 'neighborhoods-correct-results' : 0,
            'naive-queries-count' : 0, 'neighborhoods-queries-count' : 0
        }
        query_class = ''
        query_filename = ''
        result_counter = 0
        classes = {}
        is_neighborhoods = False
        f = open(file, 'r')
        for line in f:
            if "matched" in line:
                result_counter = 0
                query_class = get_query_class_from_line(line)
                query_filename = get_query_filename_from_line(line)
                log(query_class)
                if "neighborhoods" in line:
                    parse_mode = Mode.Neighborhoods
                    results['neighborhoods-queries-count'] += 1
                else:
                    parse_mode = Mode.Naive
                    results['naive-queries-count'] += 1
            else:
                if result_counter >= TOP_N or line_empty(line):
                    if len(classes) > 0:
                        clazz = sorted(classes.items(), reverse=True, key=lambda kv: kv[1])[0][0]
                        # log(' --> ' + clazz)
                        if query_class == clazz:
                            if parse_mode == Mode.Neighborhoods:
                                results['neighborhoods-correct-results'] += 1
                            else:
                                results['naive-correct-results'] += 1
                        classes.clear()
                    continue
                result_counter += 1

                answer_class = get_answer_class_from_line(line)
                answer_filename = get_answer_filename_from_line(line)
                if answer_filename == query_filename:
                    continue
                log('\t' + answer_class)
                if answer_class in classes:
                    classes[answer_class] += 1
                else:
                    classes[answer_class] = 1

        assert(results['naive-queries-count'] == results['neighborhoods-queries-count'])
        print('Class :', file)
        print('\tTotal queries            :', results['neighborhoods-queries-count'])
        print('\tAccuracy (naive)         :', round(results['naive-correct-results']/results['naive-queries-count'], 2) )
        print('\tAccuracy (neighborhoods) :', round(results['neighborhoods-correct-results']/results['neighborhoods-queries-count'], 2) )
        all_results['total_queries'] += results['naive-queries-count']
        all_results['total_naive_correct'] += results['naive-correct-results']
        all_results['total_neighborhoods_correct'] += results['neighborhoods-correct-results']
        print()
        f.close()
    print('=' * PRINT_LEN)
    print('Total queries                  :', all_results['total_queries'])
    print('Total accuracy (naive)         :', round(all_results['total_naive_correct']/all_results['total_queries'], 3))
    print('Total accuracy (neighborhoods) :', round(all_results['total_neighborhoods_correct']/all_results['total_queries'], 3))
    print('=' * PRINT_LEN)

main()
