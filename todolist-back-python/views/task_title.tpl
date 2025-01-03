% from expression import Nothing
<div>
    <h2> {{task.name}} </h2>
        % if task.execution_date:
        <p> {{task.execution_date}}</p>
        % end
        <a href="/todo/{{todolist_name}}/item/{{task.key}}/reword?{{query_string}}">Renommer</a>
        <a href="/todo/{{todolist_name}}/item/{{task.key}}/postpone?{{query_string}}">Reporter</a>
        <form action="/todo/{{todolist_name}}/item/{{task.key}}/tomorrow?{{query_string}}" method="post">
            <input type="submit" value="Demain">
        </form>

    </div>
