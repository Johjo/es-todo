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
2. controller -> use case -> adapter in memory (peu / rapide) (permet de tester le back)
3. web -> controller -> use case -> adapter in memory : test de contrat (peu / rapide) (permet de tester le front)
4. adapter : test d'intégration (beaucoup / lent) (permet de tester l'intégration)
5. test e2e
    - controller -> use case -> adapter : test e2e (peu / lent) (meilleur lecture des erreurs)
    - web -> controller -> use case -> adapter : test e2e (peu / lent) (on traverse tout)

# controller creation
1. step 1 : copy use case test
2. step 2 : remove fixture
3. step 3 : introduce dependencies
4. step 4 : pass adapter from dependencies
5. step 5 : create use case factory from dependencies
6. step 6 : feed dependencies with use case factory
7. step 7 : move use case factory to method inject use case
8. step 8 : create controller
9. step 9 : extract method using use case
10. step 10 : move method to controller

Créer une image Docker
```
docker build -t todolist-back .
```

Lancer une image Docker

```
docker run -p 8091:80 -v C:\Projets\python\todo\es-todo\todolist-back-python\db:db todolist-back 
```