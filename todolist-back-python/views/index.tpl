<html>
<head>
    <title>Todo</title>
</head>
<body>

<a href="/todo/Jonathan">Jonathan</a>
<ul>
    % for todolist_name in todolist_name_set:
        <li><a href="/todo/{{todolist_name}}">{{todolist_name}}</a></li>
    % end
</ul>


Créer une todolist
<form action="/todo" method="post">
    <input type="text" name="name" value="">
    <input type="submit" value="create">
</form>
</body>
</html>