[![oc-project-shield][oc-project-shield]][oc-project-url]

[oc-project-shield]: https://img.shields.io/badge/OPENCLASSROOMS-PROJECT-blueviolet?style=for-the-badge
[oc-project-url]: https://openclassrooms.com/fr/paths/518-developpeur-dapplication-python

# Openclassrooms - Développeur d'application Python - Projet 10

Créez une API sécurisée RESTful en utilisant Django REST

![SoftDesk](https://user.oc-static.com/upload/2023/06/28/16879473703315_P10-02.png)

## Compétences évaluées

- :bulb: Sécuriser une API afin qu'elle respecte les normes OWASP et RGPD
- :bulb: Créer une API RESTful avec Django REST

## Installation et exécution du projet

### Pré-requis

- Avoir `Python`, `pip` et `pipenv` installé sur sa machine.

1. Cloner le repo

```sh
git clone https://github.com/Gregson971/oc-da-python-p10.git
```

2. Se placer dans le dossier oc-da-python-p10/SoftDesk

```sh
cd /oc-da-python-p10/SoftDesk
```

3. Activer l'environnement virtuel

```sh
pipenv shell
```

4. Installer les packages requis

```sh
pipenv install
```

5. Créer la base de données

```sh
python manage.py migrate
```

6. Lancer le serveur Django

```sh
python manage.py runserver
```

### Utilisation

Il est possible de naviguer dans l'API avec différents outils :

- la plateforme [Postman](https://www.postman.com/) ;
- l'outil de commandes [cURL](https://curl.se/) ;
- l'interface intégrée Django REST framework à l'adresse http://127.0.0.1:8000/.

### Générer un rapport flake8-html

```sh
flake8 --format=html --htmldir=flake-report
```
