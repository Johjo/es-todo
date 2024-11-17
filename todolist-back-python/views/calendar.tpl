% rebase('base.tpl')
<p>
<h2> Calendrier</h2>
<ul>
% for task in tasks:
<li>
    <p><strong>{{task.execution_date}}</strong> {{task.name}} <a href="/todo/{{todolist_name}}/item/{{task.key}}/reword?{{query_string}}">Renommer</a> <a href="/todo/{{todolist_name}}/item/{{task.key}}/postpone?{{query_string}}">Reporter</a></p>
    </li>

% end
</ul>
</p>