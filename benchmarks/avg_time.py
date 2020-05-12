import glob

def main():
    # regex_list = ["search_*_s4_f10_min10*","search_*_s4_f15_min10*", "search_*_s4_f20_min15*", "search_*_s4_f25_min20*"]
    regex_list = ["search_Washers_s2_f10_min10.txt"]
    for regex in regex_list:
        search_results = glob.glob(regex)
        avg_time(search_results, regex)

def avg_time(search_results, regex):
    real_time = 0.0
    real_times = 0.0

    file_num = 0
    for file in search_results:
        f = open(file,'r')
        file_num += 1
        # get execution time from file
        for line in f:
            if "real" in line:
                real_time = line.split('\t')[-1].strip('\n')
                real_time = real_time.strip('s')
                min_time = int(real_time.split('m')[0]) * 60
                sec_time = float(real_time.split('m')[-1])
                real_time = sec_time + min_time
                real_times += real_time
                break
        f.close()

    print(file_num)
    avg_time = real_times/len(search_results)
    print(regex + ": " + str(avg_time) + " s")

main()
