# Web Scrapping - Fouille de textes & Scrapping

**ANTELME Mathis**

## Consignes

Récupérez les données pour ce TD sur Moodle (`Corpus detourage.zip`). Ce jeu de données est composé de documents **HTML** bruts et de la version nettoyée de référence (reference) où le code source a disparu pour ne laisser que le texte et les marques de paragraphes. Vous alimenterez au fur et à mesure du TD un fichier log (txt) où vous noterez tous vos résultats Vous rendrez le code utilisé à chaque étape (nommez le de façon explicite et/ou ayez recours à un **README**) ainsi que votre log avec les différents résultats et tableaux.

## Utilisation du programme

Afin de facilement utiliser ce programme (à des fins de correction), il vous faudrat fournir les données à traiter (ici le corpus **HTML** et le corpus de référence) dans un dossier nommé `data/Corpus_detourage` à la racine du projet sous la forme de deux sous-corpus nommé `html` et `reference`.

Il faudrat aussi créer un dossier `out` qui contiendrat toutes les statistiques générées si ce dossier n'est pas présent (encore une fois à la racine du projet).

Le programme principal est situé dans le fichier `main.py` (duh) qui peut être lancé avec des arguments. On peut lancer le code de chaque exercice individuellement avec le numéro de l'exercice en argument, tout les exercices avec l'argument `all` et supprimer tout les fichiers généré avec l'argument `clean` (par défaut le programme n'execute rien).

> **Note:** Par défaut le code utilise **TOUT** les outils pour l'extraction de données ce qui peut prendre un certains temps (environ 1h30). Le programme est suffisamment intelligent pour ne pas extraire de données si le fichier de sortie existe déjà, attention si vous changez des dossiers de place;

### Exemple d'utilisation

**Exécution de l'exercice 1:**

```bash
python main.py 1
```

**Exécution de tout les exercices:**

```bash
python main.py all
```

**Nettoyage des fichiers générés:**

```bash
python main.py clean
```

<!-- TODO: ajout de la fonction de nettoyage -->

## Exercice 1 - Utilisation d'outils de détourage

Le détourage, ou extraction de texte à partir de données Web, consiste à extraire du code source **HTML** les données utiles, ici le texte. C'est une sous-tâche de la tâche du *scrapping*.

Vous allez utiliser au moins trois des outils mentionnés durant le CM, avec à *minima* **jusText** et un outil pour chaque catégorie (cf: tableau ci dessous).

<!-- TODO: ajout tableau des outils -->

Avec chacun des de ces outils vous allez extraire le contenu textuel des fichiers html bruts et le stocker dans des dossiers séparés (portant le nom de l’outil tel qu’indiqué dans le tableau 1). Veillez à ce que les marques de paragraphes soient préservées (en effet elles sont présentes dans la référence). Ajoutez au besoin des balises `<p>` au début et à la fin de chaque ligne dans le fichier généré.

Compilez pour chacun de ces outils ainsi que pour la référence (le dossier `reference`) quelques statistiques rapides sur les fichiers générés:

- Taille totale des données en nombre de lignes, moyenne et écart-type;
- Taille totale des données en nombre de caractères, moyenne et écart-type des différences par fichier;
  - Pour le dossier `reference`;
  - Puis le dossier utilisé pour chaque outil;

Repérez les fichiers pour lesquels l’écart avec la référence est particulièrement grand: fichier nettement plus grand (*bruit*) ou plus petit (*silence*). Calculez pour chaque outil la moyenne et l’écart-type de la différence de taille en caractères par rapport au fichier de référence.

---

Pour ce premier exercice on va utiliser les *wrappers* fournis sur Moodle qui vont nous permettre de traiter ces fichiers en utilisant les différents outils. On va donc développer un programme qui va parcourir un dossier afin d'en récupérer les différents fichiers sources afin d'en extraire le contenu textuel, contenu que l'on va ensuite écrire dans un autre fichier.

Chaque outil va posséder un dossier de sortie qui lui sera attitré afin de stocker un corpus par outils, ce qui facilitera les comparaisons.

Pour effectuer les actions décrites ci-dessus, on va principalement appeller la fonction `create_subcorpus()` (dans le fichier `main.py`) qui prend en paramètre un chemin d'accès vers un corpus, un outil à utiliser et le mode de fonctionnement de l'outil.

```python
def create_subcorpus(corpus_path, tool_mode="default", tool="BP3"):

    logging.info("Scanning folder at: {} using {} tool".format(corpus_path, tool))

    # on récupère la liste des fichiers présents dans le corpus
    html_corpus = glob.glob(corpus_path + "/*")

    # on créé un dossier qui va permettre de stocker les résultats par outil
    sub_corpus_path = "./data/" + tool + "_" + tool_mode + "/raw"
    logging.info("Creating output folder at: {}".format(sub_corpus_path))
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
            logging.warn("File {} already exists, skipping".format(output_file_path))
        
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
```
<!-- TODO: ajouter le screen -->
![output_filesystem](./img/output_filesystem.png)

---

Une fois le contenu extrait du **HTML** on va pouvoir calculer des statistiques sur nos corpus. Pour cela on va utiliser le script `stats_corpus.py` qui va nous permettre de génerer les différentes statistiques.

```python
def main():

    # génération des stats pour le corpus de référence
    print(
        "{}; {}, {}".format(
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
    for key in tools.items():
        tool_corpus_path = PATH_TO_CORPUS + "/" + tools[key] + "_default/raw"
        print(
            "{}; {}, {}".format(
                tool_corpus_path,
                get_line_stats(tool_corpus_path),
                get_character_stats(tool_corpus_path),
            )
        )
```

On obtient les résultats suivants:

```bash
corpus ./data/Corpus_detourage/html; 
line_stats {'count': 2350883, 'average': 1391.8786264061575, 'deviation': 1721267.8212660826}
char_stats {'count': 127020301, 'average': 75204.44108940201, 'deviation': 2695450890.4655943}
------------
corpus ./data/BP3_default/raw; 
line_stats {'count': 317553, 'average': 188.01243339253998, 'deviation': 17601.53980988676}
char_stats {'count': 13951083, 'average': 8259.966252220249, 'deviation': 40057323.596848}
------------
corpus ./data/GOO_default/raw; 
line_stats {'count': 10831, 'average': 6.412670219064535, 'deviation': 95.98660086282653}
char_stats {'count': 2203215, 'average': 1304.449378330373, 'deviation': 4376072.847792675}
------------
corpus ./data/HTML2TEXT_default/raw; 
line_stats {'count': 567228, 'average': 335.83658969804617, 'deviation': 39892.038424367485}
char_stats {'count': 35886208, 'average': 21247.014801657784, 'deviation': 188339464.18154556}
------------
corpus ./data/INSCRIPTIS_default/raw; 
line_stats {'count': 418132, 'average': 247.5618709295441, 'deviation': 30799.639896085133}
char_stats {'count': 38072342, 'average': 22541.351095322676, 'deviation': 1287286084.5392554}
------------
corpus ./data/JT_default/raw; 
line_stats {'count': 22526, 'average': 13.336885731201894, 'deviation': 306.2020793481089}
char_stats {'count': 4186040, 'average': 2478.413262285376, 'deviation': 9447114.100380592}
------------
corpus ./data/NEWSPAPER_default/raw; 
line_stats {'count': 12749, 'average': 7.548253404381291, 'deviation': 139.9883465645637}
char_stats {'count': 2206597, 'average': 1306.4517465956187, 'deviation': 4064577.197345957}
------------
corpus ./data/NEWSPLEASE_default/raw; 
line_stats {'count': 13768, 'average': 8.151568975725281, 'deviation': 105.55665976448628}
char_stats {'count': 2894817, 'average': 1713.923623445826, 'deviation': 5126284.4684118135}
------------
corpus ./data/READABILITY_default/raw; 
line_stats {'count': 61942, 'average': 36.67377146240379, 'deviation': 6117.601686249542}
char_stats {'count': 5525811, 'average': 3271.646536412078, 'deviation': 9246772.313784612}
------------
corpus ./data/TRAF_default/raw; 
line_stats {'count': 35005, 'average': 20.725281231497927, 'deviation': 478.34844907721487}
char_stats {'count': 4159927, 'average': 2462.9526346950856, 'deviation': 5561745.44003006}
------------
corpus ./data/TRAF_BL_default/raw; 
line_stats {'count': 1689, 'average': 1.0, 'deviation': 0.0}
char_stats {'count': 4844509, 'average': 2868.270574304322, 'deviation': 9922267.444255508}
------------
corpus ./data/READ_py_default/raw; 
line_stats {'count': 26050, 'average': 15.423327412670218, 'deviation': 240.42529360564862}
char_stats {'count': 9890753, 'average': 5855.9816459443455, 'deviation': 93582972.15892889}
------------
corpus ./data/HTML-text_default/raw; 
line_stats {'count': 1689, 'average': 1.0, 'deviation': 0.0}
char_stats {'count': 12571699, 'average': 7443.2794552989935, 'deviation': 37372773.08353875}
------------
```

> **Note:** Dans un soucis de correction, le programme `main.py` peut recevoir en argument le numéro de l'exercice afin d'éviter de faire tourner tout le code à chaque fois. Si l'on souhaite lancer l'exercice 1 par example on va utiliser la commande suivante: `python main.py 1` (plus de détails dans la partie utilisation en début de document);

## Exercice 2 - Guider le scrapping avec la reconnaissance de langue

**Justext** utilise une heuristique qu’il adapte en fonction de la langue supposée du document. Quand on ne lui fournit pas la langue, il utilise son modèle par défaut ”indépendant de la langue”. Nous allons voir si nous pouvons améliorer les résultats grâce à l’integration d’un module d’identification de la langue.

Vous stockerez les résultats de cette étape dans un dossier `./data/JT_deault/langid`:

- Utilisez le module [langid.py](https://github.com/saffsd/langid.py);
- Pour chaque fichier déjà traité avec **Justext**:
  - Identifiez la langue (à partir du fichier nettoyé par **Justext** ou avec le **HTML** original);
  - Utilisez l'information sur la langue our lancer **Justext** avec le modèle de langue correspondant;
  - Stockez les fichiers ainsi obtenus dans le dossier `./data/JT_deault/langid`;

> **Note:** langid utilise les codes de langue *ISO 639-11* alors que **Justext** utilise les noms de langues en toutes lettres : *Greek (el)*, *English (en)*, *Polish (pl)*, *Russian (ru)*, *Chinese (zh)*;

Refaites la même opération en utilisant la vraie information sur la langue de chaque document qui figure sur Moodle (`doc_lg.json`). Stockez les résultats dans un dossier `./data/JT_default/trueLANG`.

Recalculez les statistiques de la fin de l’exercice précédent pour chacun des 5 dossiers, stockez les dans un tableau.

---

Pour la réalisation de cette étape on va réutiliser les wrappers fournit sur **Moodle**. Ces derniers utilisent déjà la détection de la langue par défaut pour **Justext**, on va donc modifier le comportement de `get_paragraphs_JT()` la fonction qui permet d'extraire le contenu textuel avec **Justext**. On va tout simplement lui ajouter un nouveau mode de fonctionnement qui va détecter la langue et le mode par défaut sera indépendant de langue. Etant donné qu'aucune *stopList* n'est fournie pour la langue Chinoise, on utilisera aussi le mode idépendant si cette langue est détectée.

```python
def get_paragraphs_JT(str_text, mode):
    """
    using Justext
    """
    if mode == "_english":
        stop = justext.get_stoplist("English")
    elif mode == 'lang_detect':
        lang = get_langid(str_text)
        if lang == "Chinese":
            stop = set()
        else:
            stop = justext.get_stoplist(lang)
    else:
        stop = frozenset()
    
    if len(stop) == 0:
        any_lang_stop_words = get_all_stop_words()
        paragraphs = justext.justext(str_text, any_lang_stop_words)
    else:
        paragraphs = justext.justext(str_text, stop)
    list_paragraphs = [x.text for x in paragraphs if not x.is_boilerplate]
    return list_paragraphs
```

Ensuite il ne reste plus qu'a extraire le contenu textuel en utilisant **Justext** en mode détection de langue (*lang_detect*) et par défaut (*default*).

Etant donné que la génération de statistique semble être utilisée de nombreuse fois, plutôt que de l'effectuer dans un fichier différent de manière plus ou moins propre, on va utiliser les fonctions définies précédement afin d'en créer une nouvelle dans `main.py` qui va nous permettre d'effectuer des statistiques sur tout les sous-corpus d'un dossier et de stocker ces résultats dans un fichier csv.

```python
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
```

On obtient donc les résultats suivants [ici](./out/exercice2_stats.csv):

```csv
corpus_name, line_count, line_average, line_deviation, char_count, char_average, char_deviation
HTML2TEXT_default, 567228, 335.83658969804617, 39892.038424367485, 35886208, 21247.014801657784, 188339464.18154556
JT_lang_detect, 22526, 13.336885731201894, 306.2020793481089, 4186040, 2478.413262285376, 9447114.100380592
GOO_default, 10831, 6.412670219064535, 95.98660086282653, 2203215, 1304.449378330373, 4376072.847792675
BP3_default, 317553, 188.01243339253998, 17601.53980988676, 13951083, 8259.966252220249, 40057323.596848
NEWSPAPER_default, 12749, 7.548253404381291, 139.9883465645637, 2206597, 1306.4517465956187, 4064577.197345957
TRAF_BL_default, 1689, 1.0, 0.0, 4844509, 2868.270574304322, 9922267.444255508
READ_py_default, 26050, 15.423327412670218, 240.42529360564862, 9890753, 5855.9816459443455, 93582972.15892889
HTML-text_default, 1689, 1.0, 0.0, 12571699, 7443.2794552989935, 37372773.08353875
JT_default, 22946, 13.585553582001184, 312.18939461657965, 4242854, 2512.0509177027825, 9562918.580000633
TRAF_default, 35005, 20.725281231497927, 478.34844907721487, 4159927, 2462.9526346950856, 5561745.44003006
Corpus_detourage, 0, 0, 0, 0, 0, 0
NEWSPLEASE_default, 13768, 8.151568975725281, 105.55665976448628, 2894817, 1713.923623445826, 5126284.4684118135
INSCRIPTIS_default, 418132, 247.5618709295441, 30799.639896085133, 38072342, 22541.351095322676, 1287286084.5392554
READABILITY_default, 61942, 36.67377146240379, 6117.601686249542, 5525811, 3271.646536412078, 9246772.313784612
```

> **Note:** Dans un soucis de correction, le programme `main.py` peut recevoir en argument le numéro de l'exercice afin d'éviter de faire tourner tout le code à chaque fois. Si l'on souhaite lancer l'exercice 2 par example on va utiliser la commande suivante: `python main.py 2` (plus de détails dans la partie utilisation en début de document);