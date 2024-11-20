<html>
<head>
    <meta charset="UTF-8">
    <title>Todo</title>
    <link rel="stylesheet" href="/static/todolist.css">
</head>
<body>
<div class="menu">
    <div><a href="/todo/{{todolist_name}}/calendar?{{query_string}}">Calendrier</a></div>
</div>
<div class="page">
    <div class="left">
        <div class="restart-fvp">
            <h2> Redémarrer l'algo</h2>
            <form action="/todo/{{todolist_name}}/reset?{{query_string}}" method="post">
                <input type="submit" value="Redémarrer l'algo">
            </form>
        </div>

        <div class="context-filter">
            <h2> Contexte </h2>
            <form action="/todo/{{todolist_name}}" method="get">
                <ul>
                    <li><a href="/todo/{{todolist_name}}">Supprimer les filtres</a></li>
                    % for (context, count) in counts_by_context:
                    <li> {{context}} : {{count}}</li>
                    <input type="checkbox" name="include_context" value="{{context}}" {{'checked' if context in
                    included_context else ''}}> Inclure
                    <input type="checkbox" name="exclude_context" value="{{context}}" {{'checked' if context in
                    excluded_context else ''}}> Exclure
                    % end
                </ul>
                <input type="submit" value="Filtrer">
            </form>
        </div>
        <ul>
            <li><a href="/todo/{{todolist_name}}/export">Exporter les tâches</a></li>
            <li><a href="/todo/{{todolist_name}}/import">Importer des tâches</a></li>
        </ul>
    </div>
    <div class="center">
        <div class="add-task">
            <h2> Ajouter une tâche </h2>
            <form action="/todo/{{todolist_name}}/item?{{query_string}}" method="post">
                <input type="text" name="task_name">
                <input type="submit" value="Ajouter">
            </form>
        </div>

        {{!base}}

    </div>
</div>
</body>
</html>