# Projet LITRevu

Cette application est MVP d'un projet de site web visant à échanger des critiques sur des livres et articles.

## Installation

### Clonez le dépôt

Pour cloner le dépôt, vous devrez ouvrir le terminal et effectuer la commande suivante dans le dossier de votre choix :
```bash
    git clone https://github.com/Fibuc/LITRevu.git
```

### Créez un environnement virtuel

Ensuite, vous aurez besoin de créer un environnement virtuel que vous devrez nommer `env` ou `.env` afin d'éviter son push dans le repository. Si toutefois, vous voulez utiliser un autre nom d'environnement, ajoutez-le au fichier `.gitignore`.


Ouvrez le terminal et rendez-vous dans le dossier du dépôt local du projet puis tapez la commande suivante :

```bash
    python -m venv nom_de_l_environnement
```

### Activez votre environnement virtuel

Pour activer votre environnement virtuel la méthode est différente selon votre système d'exploitation.

#### Linux & MacOS :
```bash
    source chemin_de_votre_env/bin/activate
```
#### Windows : 
```bash
    chemin_de_votre_env\Scripts\activate.bat
```

Veillez également à bien vous situer sur la branche "main" lors de l'exécution de **main.py**.

### Installez les packages

Lorsque vous aurez activé votre environnement virtuel, vous aurez également besoin d'installer les packages essentiels pour le lancement disponibles dans le requirements.txt.

```bash
    pip install -r requirements.txt
```

### Lancer le serveur

Maintenant que les packages ont été installés, on va pouvoir lancer le serveur afin de pouvoir afficher le site web.

On va se rendre dans le dossier `src` et lancer la commande suivante:

```bash
    python manage.py runserver
```
Et voilà, maintenant vous pouvez accéder à l'application via le lien: [http://localhost:8000/](http://localhost:8000/).

## Utilisation

Maintenant que l'application est lancée, vous pouvez vous inscrire en créeant un nouveau compte ou bien vous pouvez vous connecter avec ces comptes d'essais ci-dessous:

| Nom de compte | Mot de passe   | Nb ticket | Nb critique |
| :------------ |:-------------- | ---------:| -----------:|
| Jérémy47      | vh7LqV4J4Qc8n6 |         3 |           2 |
| AllanKr       | h4QcvL86V7nq4J |         3 |           0 |
| IDontKnowWho  | L6cq7Vn48hv4QJ |         2 |           1 |
| Sebseb_SF     | v6Vhq87n4QLJ4c |         1 |           3 |
| Read2Survive  | JV6Q48hcnqv7L4 |         1 |           4 |

### Flux

Lorsque vous serez connecté, vous arriverez sur la page principale, la page de Flux.

Dans cette page vous pourrez voir tous les tickets et critique que vous avez posté, les tickets postés par les utilisateurs que vous suivez ainsi que les critiques en réponse à vos tickets de vos abonnés.

Vous pourrez créer des tickets, créer des critiques à partir de zéro et des critiques en réponse à des tickets.

Vous aurez également accès à la possibilité de modifier vos différents posts.

### Posts

Dans la page des posts, vous pourrez voir tous les tickets et critiques que vous avez posté. Sur chacun de vos posts, vous aurez la possibilité de les modifier ou de les supprimer.

**Attention**: Si vous supprimez un ticket, toutes les critiques associées seront également supprimées.

### Abonnements

Enfin la dernière page est la page des abonnements. Dans cette page vous pourrez voir vos abonnés, vos abonnements avec la possibilité de ne plus suivre l'utilisateur ainsi qu'une barre de recherche afin de trouver des utilisateurs à suivre.

En suivant un utilisateur, vous aurez accès à tous ses posts.

### Déconnexion

Enfin vous pourrez vous déconnecter et vous serrez automatiquement redirigé vers la page de connexion.

## Accès à l'interface administrateur

Pour accéder à l'interface administrateur, vous devrez vous rendre sur le lien [http://localhost:8000/admin](http://localhost:8000/admin/) et vous connecter avec les identifiants de connexion administrateur.

| Nom de compte | Mot de passe   |
| :------------ |:-------------- |
| admin         | 6Q4JL8qv7nhVc4 |

Une fois connecté, vous aurez l'accès à l'interface administrateur pour gérer:
 - Les utilisateurs
 - Les suivis utilisateurs
 - Les tickets
 - Les critiques

## Générez un rapport flake8

L'application a été contrôlée par flake8. Vous trouverez le rapport en ouvrant le fichier "index.html" se trouvant dans le dossier `flake8_rapport`.

Pour générer un nouveau rapport flake8 de l'application en format HTML, vous devrez ouvrir votre terminal et vous rendre à la racine de l'application puis utiliser la fonction suivante:

```bash
    flake8 --format=html --htmldir=flake8_rapport
```

Ce nouveau rapport sera généré dans le dossier "flake8_rapport".
