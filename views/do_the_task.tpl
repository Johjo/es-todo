<html>
<head>
    <title>Todo</title>
</head>
<body>

<p>
<h2> {{task_name}} </h2>
    <form action="/todo/{{todolist_name}}/item/{{task_id}}/close" method="post">
    <input type="submit" value="C'est fait">
    </form>
</p>

Ajouter une tâche
<form action="/todo/{{todolist_name}}/item" method="post">
    <input type="text" name="item">
    <input type="submit" value="Add item">
</form>

hello from template
</body>
</html>