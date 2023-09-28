# Creation d'utilisateurs, de groupes affectation des utilisateurs à des groupes

> Retrouver une version plus facilement lisible de ce document ici : https://github.com/lorne-univ/etrs514/blob/main/CM-TD/exercice2.md

Dans cet exercice vous allez créer des utilisateur et des groupes
Avant de commencer, vérifier que vous avez bien la dernière version des fichiers d'énoncé et de validation: 
```
cd ~/etrs514
git pull
```

## Initialisation

Avant de commencer l'exercice, exécuter la commande `~/etrs514/CM-TD/exercice2.py init --step step0`
> Si vous voulez recommencer l'exercice, vous pouvez exécuter à nouveau cette commande pour repartir d'un environnement "vierge"

## Ennoncé

### Etape 1 : Création d'un utilisateur
- Créer l'utilisateur **user1** et affecter lui le mot de passe **user1**.
- Vérifier :
```
sudo /home/etudiant/etrs514/CM-TD/exercice2.py check --step step1
```

On va voir que lorsqu'un processus est exécuté, il est bien associé à l'utilisateur qui l'a lancé. 
- Ouvrir un nouvel onglet dans MobaXterm.
- Démarrer une nouvelle connexion ssh à votre machine virtuelle en tant qu'utilisateur **user1**.
- Lancer la commande sleep 360
- Démarrer une nouvelle connexion ssh à votre machine virtuelle en tant qu'utilisateur **user1**.
- Afficher la liste de tous les processus et filtrer sur la chaîne user1 en exécutant la commande `ps aux | grep user1`
- Vérifier que vous voyez bien une ligne `user1      38295  0.0  0.1 220956  1024 pts/8    S+   15:48   0:00 sleep 500`

On va maintenant vérifier à quel(s) groupe(s) appartient l'utilisateur nouvellement créé.
- Visualiser le contenu du fichier présent dans /etc, contenant la liste des groupes et pour chaque groupe donnant les utilisateurs qui sont associés.
- Vérifier que ce fichier contient une ligne ressemblant à `user1:x:1002:`
> On note que l'utilisateur user1 n'est pas noté comme appartenant au groupe user1. C'est normal, lorsque le groupe est le groupe primaire d'un utlisateur, l'utilisateur n'apparaît pas.
- En utilisant la commande `id -gn` vérifier que user1 est bien le groupe primaire de user1.
- Pour réinitialiser cette étape : 
```
sudo /home/etudiant/etrs514/CM-TD/exercice2.py init --step step1
```

### Etape 2 : Première approche des permissions sur les fichiers et les dossiers
 - En tant qu'utilisateur root, créer un dossier **/test1**
 - Le résultat de la commande `ls -l /` doit avoir une ligne ressemblant à la suivante : `drwxr-xr-x.   2 root root    6 23 sept. 16:26 test1`
 - En tant qu'utilisateur **user1**, essayer de créer un fichier **/test1/user1.txt**. Vous devriez obtenir un message ` Permission non accordée`.
 - Modifier les permissions pour que tous les utilisateurs du système aient la permission d'écrire dans le dossier **/test1**.
 - Après la modification des permissions le résultat de la commande `ls -l /` doit avoir une ligne ressemblant à la suivante : `drwxrwxrwx.   2 root root    6 23 sept. 16:26 test1`
 - En tant qu'utilisateur **user1**, essayer de créer un fichier **/test1/user1.txt**. Ca doit fonctionner.
 - Ecrire dans le fichier : **Premier test de user1.**
 - Vérifier :
```
sudo /home/etudiant/etrs514/CM-TD/exercice2.py check --step step2
```



## Vérification

- Pour vérifier votre travail, exécuter la commande `sudo /home/etudiant/etrs514/CM-TD/exercice2.py check`.
> Attention, la vérification n'est pas exhaustive. Il faut avant tout que vous ayez bien compris votre travail.