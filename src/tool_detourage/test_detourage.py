import glob
import os
from detourage import *

# permet d'ouvrir un fichier et d'en extraire le contenu
def open_file(path):
    try:
        f = open(path, "r", encoding="utf-8")
        str_text = f.read()
    except:
        f = open(path, "r", errors="ignore")  ##encoding problems
        str_text = f.read()
    f.close()
    return str_text


liste_html = glob.glob("./data/Corpus_detourage/html/*")

f = open(liste_html[0])  ##Attention spécifier encoding='utf-8' sur windows
chaine = f.read()
f.close()
### pour régler les problèmes d'encoding voir aussi la fonction open_file

liste_par = apply_tool("BP3", chaine)
print("paragraphes extraits avec BP3:")
for par in liste_par:
    print(par[:20], "...")


### la liste des noms des outils et des modes disponibles est disponible dans "tool_modes.json"

# pour avoir juste les noms :
import json

f = open("./src/tool_detourage/tool_modes.json")
dic = json.load(f)
f.close()

print("-" * 10)
print(dic.items())


