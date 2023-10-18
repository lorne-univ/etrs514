# Creation d'utilisateurs, de groupes affectation des utilisateurs à des groupes

> Retrouver une version plus facilement lisible de ce document ici : https://github.com/lorne-univ/etrs514/blob/main/CM-TD/exercice2.md

Dans cet exercice vous allez mettre en place des permissions sur des fichiers et dossiers pour un groupe d'utilisateurs travaillant sur le même projet.

Avant de commencer, vérifier que vous avez bien la dernière version des fichiers d'énoncé et de validation: 
```
cd ~/etrs514
git pull
```

## Initialisation

Si vous avez déjà commencé l'exercice et que vous voulez le recommencer en partant d'un environnement "vierge",exécuter la commande `~/etrs514/CM-TD/exercice2.py init --step all`.

### Etape 1 : Création d'un utilisateur

> Pour initialiser cette étape : `sudo /home/etudiant/etrs514/CM-TD/exercice2.py init --step step1`.
> <br> Cette commande est utile **uniquement** si vous souhaitez recommencer l'étape 1.


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
- Visualiser le contenu du fichier présent dans */etc*, contenant la liste des groupes et, qui pour chaque groupe donnant les utilisateurs qui lui sont associés.
- Vérifier que ce fichier contient une ligne ressemblant à `user1:x:1002:`
> Normalement après les derniers **:**, il y a la liste de tous les utilisateurs qui appartiennent à un groupe. On note que l'utilisateur **user1** n'est pas noté comme appartenant au groupe **user1**. Ca peut paraître bizarre à première vue, mais c'est normal, lorsque le groupe est le groupe primaire d'un utilisateur, l'utilisateur n'apparaît pas dans la liste.
- En utilisant la commande `id -gn` vérifier que **user1** est bien le groupe primaire de **user1**.

- Il n'y a rien à vérifier pour cette étape.


### Etape 2 : Première approche des permissions sur les fichiers et les dossiers

> Pour initialiser cette étape : `sudo /home/etudiant/etrs514/CM-TD/exercice2.py init --step step2`.
> <br> Cette commande doit être utilisée **uniquement** si vous n'êtes pas sûr que ce que vous avez réalisé à l'étape précédente est correct.


 - En tant qu'utilisateur root, créer un dossier **/projet1**
 - Le résultat de la commande `ls -l /` doit contenir une ligne ressemblant à la suivante : `drwxr-xr-x.   2 root root    6 23 sept. 16:26 projet1`.
 > Note : vous devez être capable de répondre à une question du type : "A quoi sert la permission x sur un dossier ?"
 - En tant qu'utilisateur **user1**, essayer de créer un fichier **/projet1/user1.txt**. Vous devriez obtenir un message ` Permission non accordée`.
 - Modifier les permissions pour que tous les utilisateurs du système aient la permission d'écrire dans le dossier **/projet1**.
 - Après la modification des permissions le résultat de la commande `ls -l /` doit avoir une ligne ressemblant à la suivante : `drwxrwxrwx.   2 root root    6 23 sept. 16:26 projet1`
 - En tant qu'utilisateur **user1**, essayer de créer un fichier **/projet1/user1.txt**. Ca doit fonctionner.
 - Ecrire dans le fichier : `Premier test de user1.`
 - Vérifier votre travail en utilisant le script de vérification :
```
sudo /home/etudiant/etrs514/CM-TD/exercice2.py check --step step2
```
 - Noter les permissions sur le fichier **/projet1/user1.txt**.
    - Propriétaire : user1
    - Groupe propriétaire : user1
    - mode : 0644

### Etape 3 : Essai de partage en local de fichiers/dossiers entre utilisateurs

> Pour initialiser cette étape : `sudo /home/etudiant/etrs514/CM-TD/exercice2.py init --step step3`.
> Remarque : cette commande est utile **uniquement** si vous n'êtes pas sûr que ce que vous avez réalisé à l'étape précédente est correct.


- Créer un deuxième utilisateur **user2** mot de passe **user2**
- En tant que **user2** créer un fichier **/projet1/user2.txt** contenant la ligne suivante **Premier test de user2.**.
- Relever les permissions sur **user2** et vérifier qu'elles correspondent bien à celles que vous vous attendiez d'avoir.
> On voit, comme ça a été dit en cours, qu'il n'y a pas d'héritage des permissions. Les permissions sont différentes de celles du dossier parent (/projet1)
- Essayer de rajouter la ligne `Premier test de user2.` à la suite dans le fichier **/projet1/user1.txt**. Vous ne devriez pas y arriver.
- En tant que **user1**, modifier les permissions sur le fichier **/projet1/user1.txt** pour faire en sorte que **user2** puisse le modifier.
- En tant que **user2**, rajouter la ligne `Deuxième test de user2.` dans le fichier **/projet1/user1.txt**.
- Modifer les permissions du fichier **/projet1/user2.txt** de telle sorte que **user1** puisse le modifier.
- En tant que **user1** ajouter la ligne `Deuxième test de user1.` dans le fichier **/projet1/user2.txt**.

- Vérifier votre travail en utilisant le script de vérification :
```
sudo /home/etudiant/etrs514/CM-TD/exercice2.py check --step step3
```

### Etape 4 : Test avec un intrus

> Pour initialiser cette étape : `sudo /home/etudiant/etrs514/CM-TD/exercice2.py init --step step4`.
> Remarque : cette commande est utile **uniquement** si vous n'êtes pas sûr que ce que vous avez réalisé à l'étape précédente est correct.


- Créer un utilisateur **intrus** mot de passe **intrus**.
- Vérifier que **intrus** peut accéder (lire et modifier) les fichiers dans le dossier **/projet1**.
- Rajouter en tant qu'intrus une ligne `Accès par intrus.` dans le fichier **/projet1/user2.txt**.
- Vérifier votre travail en utilisant le script de vérification :

```
sudo /home/etudiant/etrs514/CM-TD/exercice2.py check --step step4
```

> On constate ici deux problèmes à la solution actuelle :
> - N'importe quel utilisateur peut accéder aux fichiers/dossiers de user1 et user2.
> - Un utilisateur doit modifier manuellement les permissions pour qu'un autre utilisateur puisse y accéder.


### Etape 5 : Création d'un groupe projet1 et affectation des permissions au groupe.

> Pour initialiser cette étape : `sudo /home/etudiant/etrs514/CM-TD/exercice2.py init --step step5`.
> Remarque : cette commande est utile **uniquement** si vous n'êtes pas sûr que ce que vous avez réalisé à l'étape précédente est correct.


Pour améliorer la sécurité du dossier partagé local, il est nécessaire de :
- Placer les utilisateurs devant avoir à un dossier commun dans un groupe. 
- Spécifier dans les permissions du dossier les permissions pour le groupe.

- Créer un groupe nommé **projet1**.
- Faire en sorte que les utilisateurs **user1** et **user2** appartiennent à ce groupe comme groupe secondaire.
- Modifier, de manière récursive, le groupe d'appartenance pour le dossier **/projet1** et tous les sous-fichiers et sous-dossiers.
- Modifier, de manière récursive, les permissions sur le le dossier **/projet1** pour et tous les sous-fichiers et sous-dossiers
    - Propriétaire : (non changé) -> rwx (sur les dossiers), rw (sur les fichiers)
    - Groupe propriétaire : projet1 -> rwx (sur les dossiers), rw (sur les fichiers)
    - Autres utilisateurs : -> ---
- Se loguer en tant qu'**intrus**, vérifier qu'il n'a maintenant plus accès aux fichiers dans **/projet1**.
- Créer en tant que **user1** un nouveau fichier nommé **/projet1/user1b.txt**.
- Visualiser les permissions sur ce fichier, vous devriez avoir `-rw-rw-r--. 1 user1 user1    0 29 sept. 10:46 user1b.txt`
- Les permissions ne sont pas "idéales" :
    - On a la permission *r--* pour les *autres*. Vérifier que **intrus** ne peut pas lire le contenu du fichier, il ne peut pas car il n'a pas la permission sur le dossier **projet1**. La permission *r--* sur le fichier pour les autres utilisateurs n'est pas problématique.
    - Le dossier a comme groupre propriétaire *user1*. Essayer, en tant que **user2** de modifier contenu du fichier. **user2** ne peut pas modifier le fichier crée par **user1** alors qu'ils travaillent tous les deux sur le même projet. Ce n'est pas cohérent !!! Encore une fois c'est dû au fait que le système de gestion de fichiers Posix n'implémente pas d'héritage. Il aurait été pertinent que les fichiers créés dans **/projet1** aient comme groupe propriétaire **projet1**.
Plusieurs solutions existent à ce problème : 
- L'utilisateur change les permissions à chaque fois qu'il crée un fichier. Solution non viable.
- Un programme change les permissions automatiquement à chaque fois qu'un nouveau fichier est créé.
- Utilisation du SGID.
- Utilisation des ACL (façon actuelle et recommandée).

- Vérifier votre travail en utilisant le script de vérification :

```
sudo /home/etudiant/etrs514/CM-TD/exercice2.py check --step step5
```

### Etape 6 : ACL et héritage

> Pour initialiser cette étape : `sudo /home/etudiant/etrs514/CM-TD/exercice2.py init --step step6`.
> Remarque : cette commande est utile **uniquement** si vous n'êtes pas sûr que ce que vous avez réalisé à l'étape précédente est correct.

La machine virtuelle mise à disposition fonctionne avec un système Linux supportant les ACL. *Attention* ce n'est pas le cas de tous les systèmes.
On va donc mettre à profit cette possibilité pour configurer le dossier **/projet1**.
> On va mettre en place des acl par défaut.
- Visualiser les acl actuelles `getfacl /projet1`.
- Exécuter la commande `sudo  setfacl -d -m g:projet1:rwx,o::-- /projet1`. Cette commande fixe comme groupe par défaut **projet1** avec les permissions **rwx** et ne donne aucune permission aux autres utlisateurs.
- Exécuter la commande `ls -l /` noter le **+** qui apparaît à la fin de la ligne correspondant aux permissions projet1 `drwxrwx---+   2 root projet1   94 29 sept. 11:23 projet1`. Ce **+** indique que des ACL ont été positionnées sur le fichier. Il faut utiliser la commande `getfacl` pour connaitre les véritables permissions sur le fichier.
- En tant que **user1** créer un fichier **/projet1/user1c.txt**.
- Vérifications :
    - Vérifier que **user2** peut modifier le contenu du fichier **user1c.txt**.
    - Vérifier que **/projet1/user1c.txt** a bien des ACL de configurées (commande `ls -l`)
    - Vérifier, en utilisant la commande `getfacl /projet1/user1c.txt` que **user1c.txt** a bien les mêmes ACL par défaut que celles configurées sur le dossier parent (ici /projet1)
    
```
sudo /home/etudiant/etrs514/CM-TD/exercice2.py check --step step6
```

