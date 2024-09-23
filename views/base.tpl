<html>
<head>
    <meta charset="UTF-8">
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
<ul>
<li><a href="/todo/{{todolist_name}}/export">Exporter les tâches</a></li>
<li><a href="/todo/{{todolist_name}}/import">Importer des tâches</a></li>
</ul>



</body>
</html>