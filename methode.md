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
Avant de pouvoir passer nos transcriptions ainsi que les fichiers sons corresondants à l'aligneur automatique désiré, il faut préparer nos données. Suite aux conversions effectuées avec ELAN (pour passer du format Transcriber au format TextGrid), nous avons un fichier `TextGrid` par entretien. Or, les entretiens sont trop longs pour être passés directement à un aligneur automatique : beaucoup considère les performances d'outils comme MFA optimales sur des fragments d'audio courts (enre 5 et 15s max).
\\
Le travail de transcription, découpage d'intervales de parole étant très hétérogène d'un entretien à un autre, il y a un réel travail de segmentation à fournir, qui est particulièrement chronophage, mais nécessaire, si on veut finalement avoir de bons résultats.
\\
Ainsi, une fois le travail de segmentation des tours de parole finis : on veut découper les fichiers TextGrid et .wav en fonction des tours de parole. C'est l'idée du script `aligner_corpus_praatio.py`, exécutable en ligne de commande. Les TextGrids sont générés à partir du module python `praatio`. Pour des raisons techniques que j'ignore encore, MFA ne parvient pas à lire les fichiers générés par le module `textgridtools` (`tgt`), qui me semblait à première vue plus pratique que `praatio`. L'entretien audio est segmenté grâce au module `pydub`.

LIGNE DE COMMANDE : `./scripts-python/aligner_corpus_praatio.py PATH/TO/TG PATH/TO/WAV`