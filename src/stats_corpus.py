import glob
import json

def variance(data, ddof=0):
    n = len(data)
    if n == 0:
        return 0
    else:
        mean = sum(data) / n
        return sum((x - mean) ** 2 for x in data) / (n - ddof)

def get_file_line_total(file_path):
    """
    Retourne le nombre de ligne d'un fichier
    """
    with open(file_path, "r", encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        file.close()

    return len(lines)


def get_file_character_total(file_path):
    """
    Retourne le nombre de caractère d'un fichier
    """
    sum = 0
    with open(file_path, "r", encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        file.close()

    for line in lines:
        sum += len(line)

    return sum


def get_corpus_line_count(corpus_path):
    """
    Retourne un tableau contenant le nombre de ligne de chaque fichier d'un corpus
    """
    corpus = glob.glob(corpus_path + "/*")
    line_count = list()

    for file_path in corpus:
        line_count.append(get_file_line_total(file_path))

    return line_count


def get_corpus_character_count(corpus_path):
    """
    Retourne un tableau contenant le nombre de caractères de chaque fichier d'un corpus
    """
    corpus = glob.glob(corpus_path + "/*")
    character_count = list()

    for file_path in corpus:
        character_count.append(get_file_character_total(file_path))

    return character_count


def get_corpus_line_average(corpus_path):
    """
    Retourne la moyenne du nombre de ligne d'un corpus
    """
    line_count = get_corpus_line_count(corpus_path)
    return 0 if len(line_count) == 0 else sum(line_count) / len(line_count)


def get_corpus_character_average(corpus_path):
    """
    Retourne la moyenne du nombre de caractères d'un corpus
    """
    character_count = get_corpus_character_count(corpus_path)
    return 0 if len(character_count) == 0 else sum(character_count) / len(character_count)


def get_corpus_line_deviation(corpus_path):
    """
    Retourne l'écart-type du compte de ligne d'un corpus
    """
    return variance(get_corpus_line_count(corpus_path))


def get_corpus_character_deviation(corpus_path):
    """
    Retourne l'écart-type du compte de caractères d'un corpus
    """
    return variance(get_corpus_character_count(corpus_path))

def get_line_stats(corpus_path):
    """
    Retourne des statistiques concernant les lignes d'un corpus
    """
    results = dict()
    results["count"] = sum(get_corpus_line_count(corpus_path))
    results["average"] = get_corpus_line_average(corpus_path)
    results["deviation"] = get_corpus_line_deviation(corpus_path)
    return results


def get_character_stats(corpus_path):
    """
    Retourne des statistiques concernant les caractères d'un corpus
    """
    results = dict()
    results["count"] = sum(get_corpus_character_count(corpus_path))
    results["average"] = get_corpus_character_average(corpus_path)
    results["deviation"] = get_corpus_character_deviation(corpus_path)
    return results


###########################################################################

PATH_TO_CORPUS = "./data"

def main():

    # génération des stats pour le corpus de référence
    print(
        "corpus {}; \t\nline_stats {}\t\nchar_stats {}\n------------".format(
            './data/Corpus_detourage/html',
            get_line_stats('./data/Corpus_detourage/html'),
            get_character_stats('./data/Corpus_detourage/html'),
        )
    )

    # on récupère les différents outils disponibles
    f = open("./src/tool_detourage/tool_modes.json")
    tools = json.load(f)
    f.close()

    # on affiche toutes les statistiques pour les corpus généré par des outils
    for key, value in tools.items():
        tool_corpus_path = PATH_TO_CORPUS + "/" + key + "_default/raw"
        print(
            "corpus {}; \t\nline_stats {}\t\nchar_stats {}\n------------".format(
                tool_corpus_path,
                get_line_stats(tool_corpus_path),
                get_character_stats(tool_corpus_path),
            )
        )

if __name__ == "__main__":
    main()