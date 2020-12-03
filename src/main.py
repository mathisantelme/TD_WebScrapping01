import glob
from os import path, makedirs
import logging
import json
from stats_corpus import get_character_stats, get_line_stats
import sys

from tool_detourage.detourage import apply_tool  # on importe nos outils de détourage

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
        file_name = file_path.split("/")[
            -1
        ]
        output_file_path = sub_corpus_path + "/clean_" + file_name + ".txt"

        # si le fichier de sortie existe déjà on passe au suivant
        if path.exists(output_file_path):
            logging.warning("File {} already exists, skipping".format(output_file_path))
        
        # sinon on extrait le contenu textuel du fichier
        else:

            logging.info("Processing file: {}".format(file_path))

            # le contenu html du fichier actuel
            html_file_content = open_file(
                file_path
            )

            # on récupère la liste des paragraphes
            text_paragraphs = apply_tool(
                tool, html_file_content, mode=tool_mode
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
    corpus_stats = dict() # le dictionnaire qui contient nos statistiques ([corpus_name]: (line_stats, char_stats))

    file_list = glob.glob(PATH_TO_CORPUS + '/*') # on récupère la liste des fichiers dans le corpus de données
    for file_path in file_list:
        # on vérifie si le fichier actuel est un dossier (donc un sous-corpus)
        if path.isdir(file_path):
            logging.info('Found corpus at: {}'.format(file_path))

            # on créé un nom de corpus
            tool_corpus_path = file_path + "/raw"
            # on stocke nos statistiques dans un dictionnaire
            corpus_stats[tool_corpus_path] = (get_line_stats(tool_corpus_path), get_character_stats(tool_corpus_path)) 

    # on stocke nos stats
    with open(output_file_path + '_stats.csv', mode='w', encoding='utf-8', errors='ignore') as output_file:
        
        # on écrit nos entetes afin de faciliter la lecture du fichier
        output_file.write('corpus_name, line_count, line_average, line_deviation, char_count, char_average, char_deviation\n')

        for key in corpus_stats:
            output_string = key.split('/')[2]

            for index in range(len(corpus_stats[key])):
                for value in corpus_stats[key][index].values():
                    output_string += (', ' + str(value))

            output_file.write(output_string + '\n')

        logging.info('Stats for {} were written to {}'.format(path_to_corpus, output_file_path))

        output_file.close()

##########################################################################

PATH_TO_CORPUS = './data'
REFERENCE_CORPUS_PATH = "./data/Corpus_detourage/html"
OUTPUT_FOLDER = './out/'

logging.basicConfig(filename="./logs/main.log", level=logging.INFO)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        logging.error('No arguements specified, quitting')
        sys.exit()
    elif str(sys.argv[1]) == '1':
        logging.info('Launching code for Exo1')

        # Exercice 1 - Scrapping
        # on récupère les différents outils disponibles
        f = open("./src/tool_detourage/tool_modes.json")
        tools = json.load(f)
        f.close()

        for key, value in tools.items():
            create_subcorpus(REFERENCE_CORPUS_PATH, tool=key)
            pass

        # on génère nos stats et on les stocke dans un fichier
        generate_corpus_stats(PATH_TO_CORPUS, OUTPUT_FOLDER + 'exercice1')
    elif str(sys.argv[1]) == '2':
        logging.info('Launching code for Exo2')

        # Exercice 2 - Scrapping guide
        # on effectue le scrapping avec JT en mode default et lang_detect
        create_subcorpus(REFERENCE_CORPUS_PATH, tool='JT', tool_mode='default')
        create_subcorpus(REFERENCE_CORPUS_PATH, tool='JT', tool_mode='lang_detect')

        # on génère nos stats et on les stocke dans un fichier
        generate_corpus_stats(PATH_TO_CORPUS, OUTPUT_FOLDER + 'exercice2')
    else:
        logging.error('Arguement {}, is not recognised, quitting'.format(str(sys.argv[1])))
        sys.exit()
