import glob

def get_char_file(file_path):
    file = open(file_path, 'r', encoding='utf-8', errors='ignore')
    res = 0
    for line in file.readlines():
        res += len(line)

    return res

def get_char_total(path_to_folder):
    res = 0
    file_path_list = glob.glob(path_to_folder + '/*')
    for file_path in file_path_list:
        res += get_char_file(file_path)

    return res

def get_char_average(path_to_folder):
    res = list()
    file_path_list = glob.glob(path_to_folder + '/*')
    for file_path in file_path_list:
        res.append(get_char_file(file_path))

    return round(sum(res)/len(res), 2)

def get_stats_for_corp(corpus_path, corpus_name):
    print("{} corpus stats:".format(corpus_name))
    print("total chars in corpus: {}".format(get_char_total(corpus_path)))
    print("average char count in corpus: {}\n".format(get_char_average(corpus_path)))

get_stats_for_corp('./data/justext/raw', 'justext')
get_stats_for_corp('./data/Corpus_detourage/reference', 'reference')
