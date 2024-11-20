% rebase('base.tpl')

<div class="do-task">
    <div class="main-task">
    % include('task_title', task_name=task_name, task_id=task_id)
    <form action="/todo/{{todolist_name}}/item/{{task_id}}/close?{{query_string}}" method="post">
        <input type="submit" value="C'est fait">
    </form>

    % include('cancel_priority_button', task_key=task_id)
    </div>
</div>


