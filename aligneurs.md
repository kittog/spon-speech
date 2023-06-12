## Aligneurs automatiques
---
Quelques aligneurs automatiques à notre disposition : 
- WebMaus (interface web)
- ELAN (logiciel)
- EasyAlign (Windows) : alignement automatique avec Praat
- Montreal Forced Aligner (MFA)

#### WebMaus
Entrée : .txt et .wav correspondant ; sortie : .TextGrid avec trois tiers (découpage par mots, écriture phonétique correspondante, découpage par phonème). \\
Normes noms de fichier à respected : privilégier underscores, pas de parenthèses ("(ENQ)"), garder les mêmes normes pour les audios comme pour les fichiers .txt afin que WebMaus les traite comme paires.
Inconvénients : interface web, chargement des fichiers et alignement prennent beaucoup de temps. (10 min / 30 min)
Premiers résultats prometteurs, malgré quelques petits décalages qu'on ne peut pas empêcher.

#### Montreal Forced Aligner (MFA)
MFA = *command line utility*, *forced alignement of speech datasets*
Basé sur Kaldi (*toolkit for speech recognition*)
Plusieurs modèles (G2P, tokenizers, ivectors...).
Entrée : accepte .TextGrid, .wav (besoin d'un dossier d'entrée "corpus"); sortie : .TextGrid avec phonétiques.
Avantage : possibilité de modifier le dictionnaire de MFA pour y ajouter les mots qu'il ne connaît pas (contrairement à WebMaus par exemple) => étape de vérification du corpus.
