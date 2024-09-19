<html>
<head>
    <title>Todo</title>
</head>
<body>

{{response}}

Ajouter une tâche
<form action="/todo/{{todolist_name}}/item" method="post">
    <input type="text" name="item">
    <input type="submit" value="Add item">
</form>

hello from template
</body>
</html>