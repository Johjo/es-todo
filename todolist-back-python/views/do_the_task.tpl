% rebase('base.tpl')
<p>
    % include('task_title', task_name=task_name, task_id=task_id)
    <form action="/todo/{{todolist_name}}/item/{{task_id}}/close?{{query_string}}" method="post">
        <input type="submit" value="C'est fait">
    </form>

    <form action="/todo/{{todolist_name}}/item/{{task_id}}/cancel_priority" method="post">
        <input type="submit" value="Cette tâche n'est plus prioritaire (wip)">
    </form>
</p>

