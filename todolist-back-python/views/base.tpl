<html>
<head>
    <meta charset="UTF-8">
    <title>Todo</title>
</head>
<body>

{{!base}}

<div>
Ajouter une tâche
<form action="/todo/{{todolist_name}}/item?{{query_string}}" method="post">
    <input type="text" name="task_name">
    <input type="submit" value="Add item">
</form>
</div>

Redémarrer l'algo
<form action="/todo/{{todolist_name}}/reset?{{query_string}}" method="post">
    <input type="submit" value="Reset">
</form>

Il y a {{number_of_items}} tâches en attente.


<h2> Contexte </h2>
<ul>
<li> <a href="/todo/{{todolist_name}}?only_inbox=1">Inbox</a></li>
% for (context, count) in counts_by_context:
<li> <a href="/todo/{{todolist_name}}?context={{urlencode(context)}}">{{context}}</a> : {{count}} </li>
% end
</ul>


<ul>
<li><a href="/todo/{{todolist_name}}/export">Exporter les tâches</a></li>
<li><a href="/todo/{{todolist_name}}/import">Importer des tâches</a></li>
</ul>



</body>
</html>