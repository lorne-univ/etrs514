
# Creating files and folders

## Initialisation

Avant de commencer l'exercice, exécuter la commande `~/etrs514/exo1.py init`

## Ennoncé

- En une seule commande, créer le dossier **/home/etudiant/exercice1**.
- Dans ce dossier, en utilisant la commande ***echo*** et la redirection vers un fichier, créer un fichier nommé **exercice1_a.txt** contenant le texte : **Premier test de création de fichier**.
- Dans ce dossier, en utilisant un éditeur de texte ***nano*** ou ***vi*** ou ***vim*** créer un fichier nommé **exercice1_b.txt** contenant le texte : **Deuxième test de création de fichier**.
- Créer une copie du fichier précédent (**exercice_1b.txt**) dans le dossier **/home/etudiant**.
- Créer un fichier **/home/etudiant/exercice1/exo1.sh** contenant les lignes suivantes :
```
#!/bin/sh
for i in {1..31}
do
    echo "Line number ${i+1}"
done
```
> Ici le plus simple est d'utiliser un éditeur de texte ***nano*** ou ***vi*** ou ***vim*** et de faire un copier-coller (recherche les raccourcis clavier MobaXterm pour des copier et coller).<br>
- Rendre le script exécutable puis l'exécuter.<br>
```
./exo1.sh
```

## Vérification

- Pour vérifier, exécuter la commande `~/etrs514/exo1.py check`.