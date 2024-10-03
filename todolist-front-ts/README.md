# Todolist Front

##Procedure to add features
1. design front
2. split components
3. add slice and selector 
4. add controller

app = front

primary
hexagon = lib ??
secondary
tests = __tests__


## procedure to add feature
1. use case -> fake adapter : test métier (test unitaire) (beaucoup / rapide) (permet de créer le métier comme on en a besoin)
2. controller -> fake use case : test de contrat (peu / rapide) (permet de mettre en place le contrat)
3. controller -> use case -> fake adapter (peu / rapide) (permet de tester l'injection de dépendance)
4. adapter : test d'intégration (beaucoup / lent) (permet de tester l'intégration)
5. test e2e
    - controller -> use case -> adapter : test e2e (peu / lent) (meilleur lecture des erreurs)
    - web -> controller -> use case -> adapter : test e2e (peu / lent) (on traverse tout)