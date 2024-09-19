<html>
<head>
    <title>Todo</title>
</head>
<body>

<p>
<h2> Rien à faire </h2>
</p>

<div>
Ajouter une tâche
<form action="/todo/{{todolist_name}}/item" method="post">
    <input type="text" name="item">
    <input type="submit" value="Add item">
</form>
</div>

hello from template
</body>
</html>