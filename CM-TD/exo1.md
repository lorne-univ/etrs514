
# Creating files and folders

> Retrouver une version plus facilement lisible de ce document ici : https://github.com/lorne-univ/etrs514/blob/main/CM-TD/exo1.md

Ce premier exercice revient sur les manipulations de bases (création, édition, copie, suppression) sur les fichiers.
Vérifier que vous avez bien la dernière version des fichiers : 
```
cd ~/etrs514
git pull
```

## Initialisation

Avant de commencer l'exercice, exécuter la commande `~/etrs514/CM-TD/exo1.py init`
> Si vous voulez recommencer l'exercice, vous pouvez exécuter à nouveau cette commande pour repartir d'un environnement "vierge"

## Ennoncé

- En une seule commande, créer le dossier **/home/etudiant/exercice1**.
- Dans ce dossier, en utilisant la commande ***echo*** et la redirection vers un fichier, créer un fichier nommé **exercice1_a.txt** contenant le texte : **Premier test de création de fichier**.
- Dans ce dossier, en utilisant un éditeur de texte ***nano*** ou ***vi*** ou ***vim*** créer un fichier nommé **exercice1_b.txt** contenant le texte : 
```
Deuxième test de création de fichier.
Utilisation d'un éditeur.
C'est moins rapide mais ça fonctionne aussi.
```
> Ici le plus rapide est d'utiliser un éditeur de texte et de faire un copier-coller (recherche les raccourcis clavier MobaXterm pour des copier et coller).<br>

- Créer une copie du fichier précédent (**exercice_1b.txt**) dans le dossier **/home/etudiant**.
- Créer un fichier **/home/etudiant/exercice1/exo1.sh** contenant les lignes suivantes :
```
#!/bin/sh
for i in {1..31}
do
    echo "Line number $((${i}+2))" >> /home/etudiant/exercice1_b.txt 
done
```
> Le plus rapide est d'utiliser un éditeur de texte ***nano*** ou ***vi*** ou ***vim*** et de faire un copier-coller depuis MobaXterm<br>
- Rendre le script exécutable puis l'exécuter.<br>
```
./exo1.sh
```
- Visualiser le contenu du fichier /home/etudiant/exercice1_b.txt.
> 1. Vérifier que les trois lignes écrites avant l'exécution du script sont bien présentes.
> 2. Vérifier que le contenu du fichier correspond à celui attendu (comprendre ce que réalise le script) 
## Vérification

- Pour vérifier votre travail, exécuter la commande `~/etrs514/CM-TD/exo1.py check`.
> Attention, la vérification n'est pas exhaustive. Il faut avant tout que vous ayez bien compris votre travail.