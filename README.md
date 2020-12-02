# Web Scrapping - Fouille de textes & Scrapping

**ANTELME Mathis**

## Consignes

Récupérez les données pour ce TD sur Moodle (`Corpus detourage.zip`). Ce jeu de données est composé de documents **HTML** bruts et de la version nettoyée de référence (reference) où le code source a disparu pour ne laisser que le texte et les marques de paragraphes. Vous alimenterez au fur et à mesure du TD un fichier log (txt) où vous noterez tous vos résultats Vous rendrez le code utilisé à chaque étape (nommez le de façon explicite et/ou ayez recours à un **README**) ainsi que votre log avec les différents résultats et tableaux.

## Exercice 1 - Utilisation d'outils de détourage

Le détourage, ou extraction de texte à partir de données Web, consiste à extraire du code source **HTML** les données utiles, ici le texte. C'est une sous-tâche de la tâche du *scrapping*.

Vous allez utiliser au moins trois des outils mentionnés durant le CM, avec à *minima* **JUSTEXT** et un outil pour chaque catégorie (cf: tableau ci dessous).

<!-- TODO: ajout tableau des outils -->

Avec chacun des de ces outils vous allez extraire le contenu textuel des fichiers html bruts et le stocker dans des dossiers séparés (portant le nom de l’outil tel qu’indiqué dans le tableau 1). Veillez à ce que les marques de paragraphes soient préservées (en effet elles sont présentes dans la référence). Ajoutez au besoin des balises `<p>` au début et à la fin de chaque ligne dans le fichier généré.

Compilez pour chacun de ces outils ainsi que pour la référence (le dossier `reference`) quelques statistiques rapides sur les fichiers générés:

- Taille totale des données en nombre de lignes, moyenne et écart-type;
- Taille totale des données en nombre de caractères, moyenne et écart-type des différences par fichier;
  - Pour le dossier `reference`;
  - Puis le dossier utilisé pour chaque outil;

Repérez les fichiers pour lesquels l’écart avec la référence est particulièrement grand: fichier nettement plus grand (*bruit*) ou plus petit (*silence*). Calculez pour chaque outil la moyenne et l’écart-type de la différence de taille en caractères par rapport au fichier de référence.