# Creation d'utilisateurs, de groupes affectation des utilisateurs à des groupes

> Retrouver une version plus facilement lisible de ce document ici : https://github.com/lorne-univ/etrs514/blob/main/CM-TD/exercice2.md

Dans cet exercice vous allez créer des utilisateur et des groupes
Avant de commencer, vérifier que vous avez bien la dernière version des fichiers d'énoncé et de validation: 
```
cd ~/etrs514
git pull
```

## Initialisation

Avant de commencer l'exercice, exécuter la commande `~/etrs514/CM-TD/exercice2.py init`
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

### Etape 2 : 


## Vérification

- Pour vérifier votre travail, exécuter la commande `~/etrs514/CM-TD/exo1.py check`.
> Attention, la vérification n'est pas exhaustive. Il faut avant tout que vous ayez bien compris votre travail.