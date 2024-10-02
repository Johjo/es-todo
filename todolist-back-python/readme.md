# README

## install package with pip and pipenv
- create virtual environment `python -m pipenv shell`
- install package`python -m pip install -r requirements.txt`
- update .env file
- start backend `python web.py`


## Update requirements file
`python -m pip freeze > requirements.txt`

## procedure to add feature
1. use case -> fake adapter : test métier (test unitaire) (beaucoup / rapide) (permet de créer le métier comme on en a besoin)
2. controller -> fake use case : test de contrat (peu / rapide) (permet de mettre en place le contrat)
3. web -> controller -> fake use case : test de contrat (peu / rapide) (permet de tester le front)
4. controller -> use case -> fake adapter (peu / rapide) (permet de tester le back)
5. adapter : test d'intégration (beaucoup / lent) (permet de tester l'intégration)
6. test e2e
    - controller -> use case -> adapter : test e2e (peu / lent) (meilleur lecture des erreurs)
    - web -> controller -> use case -> adapter : test e2e (peu / lent) (on traverse tout)
