import glob
from os import path, makedirs
import logging
import json
import sys
import shutil

from tool_detourage.detourage import apply_tool  # on importe nos outils de détourage
from stats_corpus import (
    get_character_stats,
    get_line_stats,
)  # on importe les outils de generation de statistiques
from intrinseque.cleaneval_tool import (
    evaluate_file,
)  # on importe l'outil d'evaluation de fichiers

# permet d'ouvrir un fichier et d'en retourner le contenu sous forme d'une string
def open_file(path):
    try:
        f = open(path, "r", encoding="utf-8")
        str_text = f.read()
    except:
        f = open(path, "r", errors="ignore")
        str_text = f.read()
    f.close()
    return str_text


def create_subcorpus(corpus_path, tool_mode="default", tool="BP3"):

    logging.info("Scanning folder at: {} using {} tool".format(corpus_path, tool))

    # on récupère la liste des fichiers présents dans le corpus
    html_corpus = glob.glob(corpus_path + "/*")

    # on créé un dossier qui va permettre de stocker les résultats par outil
    sub_corpus_path = "./data/" + tool + "_" + tool_mode + "/raw"
    logging.info("Creating output folder at: {}".format(sub_corpus_path))

    if not path.exists(sub_corpus_path):
        makedirs(sub_corpus_path)

    # pour chaque fichier dans le corpus
    for file_path in html_corpus:

        # on construit un nom de fichier utilisé lors de l'écriture
        file_name = file_path.split("/")[-1]
        output_file_path = sub_corpus_path + "/clean_" + file_name + ".txt"

        # si le fichier de sortie existe déjà on passe au suivant
        if path.exists(output_file_path):
            logging.warning("File {} already exists, skipping".format(output_file_path))

        # sinon on extrait le contenu textuel du fichier
        else:

            logging.info("Processing file: {}".format(file_path))

            # le contenu html du fichier actuel
            html_file_content = open_file(file_path)

            # on récupère la liste des paragraphes
            text_paragraphs = apply_tool(
                tool, html_file_content, mode=tool_mode, file_name=file_name
            )

            # la variable qui sert à stocker le contenu textuel final du fichier actuel
            text_file_content = ""

            # pour chaque paragraphe du contenu extrait (on ajoute des balises de paragraphes)
            for paragraph in text_paragraphs:
                text_file_content += "<p>" + paragraph + "</p>\n"

            # on inscrit notre résultats dans un fichier
            with open(output_file_path, mode="w", encoding="utf-8") as output_file:
                output_file.write(text_file_content)
                output_file.close()

            logging.info(
                "Wrote {} lines into {}".format(
                    len(text_file_content), output_file_path
                )
            )


def generate_corpus_stats(path_to_corpus, output_file_path):
    """
    Effectue les statistiques sur les sous-corpus créés et les stockes dans un fichier désigné
    """
    corpus_stats = (
        dict()
    )  # le dictionnaire qui contient nos statistiques ([corpus_name]: (line_stats, char_stats))

    file_list = glob.glob(
        PATH_TO_CORPUS + "/*"
    )  # on récupère la liste des fichiers dans le corpus de données
    for file_path in file_list:
        # on vérifie si le fichier actuel est un dossier (donc un sous-corpus)
        if path.isdir(file_path):
            logging.info("Found corpus at: {}".format(file_path))

            # on créé un nom de corpus
            tool_corpus_path = file_path + "/raw"
            # on stocke nos statistiques dans un dictionnaire
            corpus_stats[tool_corpus_path] = (
                get_line_stats(tool_corpus_path),
                get_character_stats(tool_corpus_path),
            )

    # on stocke nos stats
    with open(
        output_file_path + "_stats.csv", mode="w", encoding="utf-8", errors="ignore"
    ) as output_file:

        # on écrit nos entetes afin de faciliter la lecture du fichier
        output_file.write(
            "corpus_name, line_count, line_average, line_deviation, char_count, char_average, char_deviation\n"
        )

        for key in corpus_stats:
            output_string = key.split("/")[2]

            for index in range(len(corpus_stats[key])):
                for value in corpus_stats[key][index].values():
                    output_string += ", " + str(value)

            output_file.write(output_string + "\n")

        logging.info(
            "Stats for {} were written to {}".format(path_to_corpus, output_file_path)
        )

        output_file.close()


def eval_intrinseque_corpus(
    corpus_path,
    clean_reference_path="./data/Corpus_detourage/reference",
    doc_lang_path="./data/doc_lg.json",
):
    """
    Permet de mesurer la correspondance entre le corpus de référence et un corpus spécifié
    """

    # la structure qui va contenir les mesures comme:
    # [langue]: dict([F]:list(int), [R]: list(int), [P]: list(int))
    measurements = dict()

    # on charge notre dictionnaire contenant nos fichiers et leur langue respective
    with open(
        doc_lang_path, mode="r", encoding="utf-8", errors="ignore"
    ) as doc_lang_file:
        lang_codes = json.load(doc_lang_file)
        doc_lang_file.close()

    # pour chaque fichier du corpus, on détecte la langue et on le compare à son fichier de référence
    file_list = glob.glob(corpus_path + "/raw/*")
    for file_path in file_list:

        # on créé le chemin du fichier de référence en fonction du fichier actuel
        file_name = file_path.split("clean_")[-1].replace(".txt", "")
        clean_file_path = clean_reference_path + "/" + file_name

        logging.info(
            "Comparing {} to clean reference: {}".format(file_path, clean_file_path)
        )

        # on récupère la langue actuelle du fichier
        current_lang = lang_codes[file_name]

        # on effectue la comparaison
        current_stats = evaluate_file(
            file_path, clean_file_path
        )  # on compare notre fichier extrait et la reference 'propre'

        # on stocke nos valeurs dans notre structure
        # si on aucun enregistrement pour la langue actuelle on créé notre dictionnaire
        if current_lang not in measurements:
            measurements[current_lang] = {"F": list(), "R": list(), "P": list()}

        measurements[current_lang]["F"].append(current_stats["f-score"])
        measurements[current_lang]["R"].append(current_stats["precision"])
        measurements[current_lang]["P"].append(current_stats["recall"])

    logging.info(
        "Comparison between {} and {} finished".format(
            corpus_path, clean_reference_path
        )
    )

    return measurements


def evaluate_all_corpus(
    corpuses_location="./data",
    reference_corpus_path="./data/Corpus_detourage/reference",
    doc_lang_path="./data/doc_lg.json",
    output_file="./out/output_evaluation.csv",
):
    """
    Permet d'évaluer les differents corpus et de stocker les resultats dans un fichier csv
    """

    # on récupère chaque corpus (sauf celui de référence)
    corpus_list = glob.glob(corpuses_location + "/*")

    results = dict()  # structure qui va stocker nos résultats finaux
    total_measurements = dict(
        {"total_F": list(), "total_R": list(), "total_P": list()}
    )  # structure pour calculer les statistiques globales

    for corpus_path in corpus_list:
        if "./data/Corpus_detourage" in corpus_path:
            pass
        elif path.isdir(corpus_path):
            corpus_name = corpus_path.split("/")[-1]  # on génère le nom du corpus
            current_results = eval_intrinseque_corpus(
                corpus_path, reference_corpus_path, doc_lang_path
            )

            # on fait les moyennes des différentes mesures
            results[corpus_name] = dict()
            results[corpus_name]["All"] = dict()
            for lang_key, lang_item in current_results.items():
                # on créé un dictionnaire pour chaque langue
                results[corpus_name][lang_key] = dict()
                for measurement_key, measurement_item in lang_item.items():
                    results[corpus_name][lang_key][measurement_key] = sum(
                        measurement_item
                    ) / len(measurement_item)

                    # on stocke toutes nos mesures pour le calcul global
                    if measurement_key == "F":
                        total_measurements["total_F"] += measurement_item
                    elif measurement_key == "R":
                        total_measurements["total_R"] += measurement_item
                    elif measurement_key == "P":
                        total_measurements["total_P"] += measurement_item
                    else:
                        logging.warning(
                            "Key {} not recognised, skipping".format(measurement_key)
                        )

        # on calcule et stocke nos mesure globale sur toutes les langues
        results[corpus_name]["All"]["F"] = sum(total_measurements["total_F"]) / len(
            total_measurements["total_F"]
        )
        results[corpus_name]["All"]["R"] = sum(total_measurements["total_R"]) / len(
            total_measurements["total_R"]
        )
        results[corpus_name]["All"]["P"] = sum(total_measurements["total_P"]) / len(
            total_measurements["total_P"]
        )

    # on stocke nos infos dans un fichier csv
    logging.info("Storing results in {}".format(output_file))

    with open(output_file, mode="w", encoding="utf-8", errors="ignore") as output:
        # on écrit nos entêtes
        output.write(
            ", all, , ,Russian, , ,Chinese, , ,English, , ,Polish, , ,Greek, , \n"
        )
        output.write(
            "Tool name, F, R, P, F, R, P, F, R, P, F, R, P, F, R, P, F, R, P\n"
        )

        for tool, lang in results.items():
            output_string = str(tool)
            for measurement in lang.values():
                output_string += ", {}, {}, {}".format(
                    measurement["F"], measurement["R"], measurement["P"]
                )
            output.write(output_string + "\n")
        output.close()

def main():
    """
    Lance le code pour tout les exercices
    """
    # Exercice 1 - Scrapping
    # on récupère les différents outils disponibles
    f = open("./src/tool_detourage/tool_modes.json")
    tools = json.load(f)
    f.close()

    for key, value in tools.items():
        create_subcorpus(REFERENCE_CORPUS_PATH, tool=key)
        pass

    # on génère nos stats et on les stocke dans un fichier
    generate_corpus_stats(PATH_TO_CORPUS, OUTPUT_FOLDER + "exercice1")

    # Exercice 2 - Scrapping guide
    # on effectue le scrapping avec JT en mode default et lang_detect
    create_subcorpus(
        REFERENCE_CORPUS_PATH, tool="JT", tool_mode="default"
    )  # indépendant de la langue
    create_subcorpus(
        REFERENCE_CORPUS_PATH, tool="JT", tool_mode="lang_detect"
    )  # détection de la langue
    create_subcorpus(
        REFERENCE_CORPUS_PATH, tool="JT", tool_mode="lang_specified"
    )  # langue spécifiée

    # on génère nos stats et on les stocke dans un fichier
    generate_corpus_stats(PATH_TO_CORPUS, OUTPUT_FOLDER + "exercice2")

    # Exercice 3
    logging.info("Launching code for Exo3")

    # on évalue tout les corpus et on stockes les résultats dans un fichier csv
    evaluate_all_corpus(corpuses_location=PATH_TO_CORPUS, reference_corpus_path=CLEAN_REFERENCE_CORPUS_PATH, doc_lang_path=DOC_LG_PATH, output_file='./out/exercice3_evaluations.csv')

##########################################################################

PATH_TO_CORPUS = "./data"
REFERENCE_CORPUS_PATH = "./data/Corpus_detourage/html"
CLEAN_REFERENCE_CORPUS_PATH = "./data/Corpus_detourage/reference"
OUTPUT_FOLDER = "./out/"
DOC_LG_PATH = "./data/doc_lg.json"

logging.basicConfig(filename="./logs/main.log", level=logging.INFO)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        logging.error("No arguements specified, quitting")
        sys.exit()
    elif str(sys.argv[1]) == "1":
        logging.info("Launching code for Exo1")

        # Exercice 1 - Scrapping
        # on récupère les différents outils disponibles
        f = open("./src/tool_detourage/tool_modes.json")
        tools = json.load(f)
        f.close()

        for key, value in tools.items():
            create_subcorpus(REFERENCE_CORPUS_PATH, tool=key)
            pass

        # on génère nos stats et on les stocke dans un fichier
        generate_corpus_stats(PATH_TO_CORPUS, OUTPUT_FOLDER + "exercice1")
    elif str(sys.argv[1]) == "2":
        logging.info("Launching code for Exo2")

        # Exercice 2 - Scrapping guide
        # on effectue le scrapping avec JT en mode default et lang_detect
        create_subcorpus(
            REFERENCE_CORPUS_PATH, tool="JT", tool_mode="default"
        )  # indépendant de la langue
        create_subcorpus(
            REFERENCE_CORPUS_PATH, tool="JT", tool_mode="lang_detect"
        )  # détection de la langue
        create_subcorpus(
            REFERENCE_CORPUS_PATH, tool="JT", tool_mode="lang_specified"
        )  # langue spécifiée

        # on génère nos stats et on les stocke dans un fichier
        generate_corpus_stats(PATH_TO_CORPUS, OUTPUT_FOLDER + "exercice2")

    elif str(sys.argv[1]) == "3":
        # Exercice 3
        logging.info("Launching code for Exo3")

        # on évalue tout les corpus et on stockes les résultats dans un fichier csv
        evaluate_all_corpus(corpuses_location=PATH_TO_CORPUS, reference_corpus_path=CLEAN_REFERENCE_CORPUS_PATH, doc_lang_path=DOC_LG_PATH, output_file='./out/exercice3_evaluations.csv')

    # on lance le code de tout les exercices
    elif str(sys.argv[1]) == "all":
        main()
    
    else:
        logging.error(
            "Arguement {}, is not recognised, quitting".format(str(sys.argv[1]))
        )
        sys.exit()
