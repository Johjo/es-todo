% from expression import Nothing
<div>
    <h2> {{task.name}} </h2>
        % if task.execution_date != Nothing:
        <p> {{task.execution_date}}</p>
        % end
        <a href="/todo/{{todolist_name}}/item/{{task.id}}/reword?{{query_string}}">Renommer</a> <a href="/todo/{{todolist_name}}/item/{{task.id}}/postpone?{{query_string}}">Reporter</a>
    </div>
