<html>
<head>
    <title>Todo</title>
</head>
<body>

<p>
<h2> {{name_1}}</h2>
<form action="/todo/{{todolist_name}}/item/choose/{{index_1}}/ignore/{{index_2}}" method="post">
    <input type="submit" value="Choisir cette tâche">
</form>

<form action="/todo/{{todolist_name}}/item/{{index_1}}/close" method="post">
    <input type="submit" value="C'est fait">
</form>
</p>

<p>
<h2> {{name_2}}</h2>
<form action="/todo/{{todolist_name}}/item/choose/{{index_2}}/ignore/{{index_1}}" method="post">
    <input type="submit" value="Choisir cette tâche">
</form>

<form action="/todo/{{todolist_name}}/item/{{index_2}}/close" method="post">
    <input type="submit" value="C'est fait">
</form>
</p>


<h2> Ajouter une tâche </h2>
<form action="/todo/{{todolist_name}}/item" method="post">
    <input type="text" name="item">
    <input type="submit" value="Add item">
</form>
</body>
</html>