<html>
<head>
    <title>Todo</title>
</head>
<body>

{{!base}}

<div>
Ajouter une tâche
<form action="/todo/{{todolist_name}}/item" method="post">
    <input type="text" name="item">
    <input type="submit" value="Add item">
</form>
</div>

Redémarrer l'algo
<form action="/todo/{{todolist_name}}/reset" method="post">
    <input type="submit" value="Reset">
</form>

Il y a {{number_of_items}} tâches en attente.

</body>
</html>