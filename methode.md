## Choix de l'aligneur automatique
---
**Possibilités** :
- Webmaus (plateforme en ligne/web) : prend en entrée fichier .txt et .wav
- Montreal Forced Aligner, ou MFA (à installer) : prend en entrée .txt/.TextGrid et .wav
- ELAN
- EasyAlign (uniquement disponible pour Windows)

## Préparation des données
---
### Première segmentation semi-automatique avec Praat
Comme présenté dans le document `annexe.md`, l'une des conventions de transcription posant problème est celle des pauses (symbolisée par des +/+++ ou indiquées entre crochets). On veut des tours de parole pas trop longs (plus facile à gérer avec les aligneurs par la suite).
Script `pause_segmentation.praat` : indique à l'utilisateur où sont les pauses dans le TextGrid et lui permet de le modifier directement sur praat. (au moyen d'une boucle) De même si un intervalle de parole est "trop long" (seuil à déterminer). Ceci permet de semi-automatiser le travail.

### Découpage des fichiers TextGrid et wav
Avant de pouvoir passer nos transcriptions ainsi que les fichiers sons corresondants à l'aligneur automatique désiré, il faut préparer nos données. Suite aux conversions effectuées avec ELAN (pour passer du format Transcriber au format TextGrid), nous avons un fichier `TextGrid` par entretien. Or, les entretiens étant relativement longs (de 45min à 1h30), les fichiers `.wav` sont trop lourds, ce qui risque de mettre en difficulté l'aligneur automatique et de générer un certains nombres d'erreurs.
\\
Ainsi : on veut découper les fichiers TextGrid et .wav en fonction des tours de parole. C'est l'idée du script `textgrid_to_txt.py` (à optimiser). Ce dernier comprends trois fonctions : 
- `divide` : prend en entrée une "entry" (objet de praatIO) => correspond à un tour de parole. créer une nouvelle textgrid à partir de l'entrée. extrait du fichier .wav un nouveau fichier `.wav` sur l'intervalle de l'entrée (xmin, xstart dans le TextGrid ; `entry.start`, `entry.end` avec praatIO)
- `label_to_txt` : ouvre la nouvelle textgrid générée, en extrait le texte (*label*) pour le stocker dans un fichier `.txt` (étape utile uniquement pour Webmaus, pour MFA on peut se contenter des TextGrid)
- `divide_and_write` : prend en entrée deux listes de chemin de fichiers (TextGrid et .wav), ouvre les TextGrid un à un, parcourt les tiers, puis les intervalles (entries), afin d'exécuter les fonctions `divide` et `label_to_txt`.
- *Dernière étape d'optimisation* : utiliser `argparse` pour exécuter le script en ligne de commande (depuis le terminal)

Toutes ces étapes se font *suite au nettoyage des fichiers* avec le script `clean_textgrid.py` (ou `.praat`).