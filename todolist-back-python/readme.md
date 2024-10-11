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
2. controller -> use case -> fake adapter (peu / rapide) (permet de tester le back)
3. web -> controller -> use case -> fake adapter : test de contrat (peu / rapide) (permet de tester le front)
4. adapter : test d'intégration (beaucoup / lent) (permet de tester l'intégration)
5. test e2e
    - controller -> use case -> adapter : test e2e (peu / lent) (meilleur lecture des erreurs)
    - web -> controller -> use case -> adapter : test e2e (peu / lent) (on traverse tout)


# step 1 : copy use case test
# step 2 : remove fixture
# step 3 : introduce dependencies
# step 4 : pass adapter from dependencies
# step 5 : create use case factory from dependencies
# step 6 : feed dependencies with use case factory
# step 7 : move use case factory to method inject use case
# step 8 : create controller
# step 9 : extract method using use case
# step 10 : move method to controller
