% rebase('base.tpl')
<p>
    % include('task_title', task_name=task_name, task_id=task_id)
    <form action="/todo/{{todolist_name}}/item/{{task_id}}/close" method="post">
    <input type="submit" value="C'est fait">
    </form>
</p>

