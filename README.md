# spon-speech
Travail réalisé dans le cadre de mon stage au Laboratoire de Phonétique et Phonologie.
> **Encadrant** : Cédric Gendrot
> 
> **Sujet** : *Analyse sociolinguistique des corpus ESLO et CFPP pour des catégories socio-professionnelles, niveau d'étude, etc*
> 
> **Dates stage** : 15 mai au 31 juillet 2023

### Guide
- `scripts-praat` et `scripts-python` : dossiers contenants respectivement les scripts praat et python.
    - `scripts-praat`
        - `clean_textgrid.praat` : nettoyage des fichiers TextGrid (avec regex),
        - `pause_segmentation.praat` : script à terminer si possible ; l'idée était d'automatiser la recherche d'intervalles de parole trop longs sur un TextGrid, afin de pouvoir les segmenter. Finalement, réaliser le processus manuellement n'est pas plus mal.
    - `scripts-python`
        - `clean_textgrid.py` : nettoyage des TextGrid (regex) ;
        - `aligner_corpus_praatio.py` : génère corpus de fichiers .wav et .TextGrid (ou .txt) à partir d'un couple de fichiers .wav et .TextGrid donné pour l'alignement automatique. Génération des TextGrid avec le module `praatio` ;
        - `aligner_corpus.py` : génération des TextGrid avec `textgridtools` ;
        - `open_smile_test.ipynb` : notebook d'exploration du module openSMILE (extraction de features, graphique avec seaborn) ;
        - `overlaps.py` : supprimer les chevauchements dans un fichier TextGrid.

- `TextGrid-corpus` : corpus TextGrid post conversion des fichiers .trs (Transcriber).
- `TextGrid-clean` : corpus TextGrid après "nettoyage", segmentation des tours de parole, sans la tier ENQ.
