import justext
import glob
import os.path
import logging

CORPUS_PATH = './data/Corpus_detourage/html'
RESULTS_PATH = './data/justext/raw'
file_path_list = glob.glob(CORPUS_PATH + '/*') # on récupère la liste des fichiers de notre corpus

# on définit un logger
logging.basicConfig(filename='./logs/exo1_justext.log', level=logging.INFO)

# on récupère tout les stopwords
def get_all_stop_words():
  stop_words = set()
  for language in justext.get_stoplists():
      stop_words.update(justext.get_stoplist(language))
  return stop_words

for file_name in file_path_list:
    file_html = open(file_name, 'r', encoding='utf-8', errors='ignore') # on ouvre le fichier pour le lire
    file_content_html = file_html.read() # on récupère le contenu HTML de la page

    # on récupère les paragraphes
    file_paragraphs = justext.justext(str(file_content_html), get_all_stop_words())
    
    logging.info("=== Reading file {} ===".format(file_name))

    # on ouvre un fichier d'écriture pour stocker les informations lues
    output_file_name = RESULTS_PATH + '/' + file_name.split('/')[4] + '_clean.txt'

    # si le fichier existe déjà on ne le réécrit pas et on passe au suivant
    if os.path.exists(output_file_name):
        logging.info('[Info] - File {} already exsits, skipping;'.format(output_file_name)) # si le fichier existe déjà alors on passe au suivant
    
    # si il n'existe pas alors on le créé
    else:
        with (open(output_file_name, 'w', encoding='utf-8')) as output_file:
            file_content_txt = '' # le contenu textuel de la page

            for paragraph in file_paragraphs:
                # si le paragraphe actuel n'est pas une boilerplate alors on l'ajoute dans notre string de contenu textuel (un paragraphe par ligne)
                if not paragraph.is_boilerplate:
                    file_content_txt += '<p>' + paragraph.text.replace("\n", '') + '</p>\n'

            logging.info('Writing {} lines to -> {}'.format(len(file_content_txt), output_file_name))
            
            # on écrit notre contenu dans notre fichier et on le ferme
            output_file.write(file_content_txt)
            output_file.close()