## Quelques mots sur les transcriptions du CFPP
--- 
Les transcriptions des fichiers audios du CFPP ayant été réalisées par différentes personnes, sans suivre les mêmes conventions d'écriture, il était plus que nécessaire de tout d'abord procéder à un travail d'homogénisation (~nettoyage de chaînes de caractères). 

Deux scripts implémentés pour traiter cette tâche : `clean_textgrid.py` et `clean_textgrid.praat`. Ils traitent tous les motifs repérés, à l'exception des doutes du transcripteur.

### Différents motifs repérés et modifications envisagées :
- **pauses** : \[pause\], {pause} ou alors + (pause "courte"), +++ (pause "longue")
    - on coupe la transcription au niveau de la pause ? (pause => \n)
- **"didascalies"** : \[rires\], \[pff\], \[hhh\], {rires}...
    - suppression des didascalies
- **clitiques** : "j'\s" (apostrophe toujours suivie d'un espace)
    - écrire pronom en entier : j' => je, c' => ce...
- **hésitations** : mm, mh, hmm, mmm (différentes orthographes)
    - remplacer toute hésitation par "euh".
- **doutes du transcripteur** : /ou, où/
    - on traitera à posteriori.
- **lien entre deux bouts de phrase après une didascalie** :

    > *y a le manège \[mm\] +y a un coin pour pique-niquer c'est vrai que \[mm\]*
    - motif : \[\w*\] +\w
    - à supprimer
- **mots non-retranscrits** : XX, XXX... indiquent les mots de 2 à 3 syllabes non retranscrits car inaudible ou autre.
    - on traitera à posteriori.
- **discours rapporté** : 
    >*elle me dit \[""\] blablabla \[""\]*
    - supprimer les crochets et garder les guillemets ?