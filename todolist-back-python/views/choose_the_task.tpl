% rebase('base.tpl')
<div class="choose-task">
    <div class="main-task">
        % include('task_title', task=task_1)
        <form action="/todo/{{todolist_name}}/item/choose/{{task_1.key}}/ignore/{{task_2.key}}?{{query_string}}" method="post">
            <input type="submit" value="Choisir cette tâche">
        </form>

        % include('cancel_priority_button', task_key=task_1.key)

        <form action="/todo/{{todolist_name}}/item/{{task_1.key}}/close?{{query_string}}" method="post">
            <input type="submit" value="C'est fait">
        </form>
    </div>

    <div class="secondary-task">
        % include('task_title', task=task_2)
        <form action="/todo/{{todolist_name}}/item/choose/{{task_2.key}}/ignore/{{task_1.key}}?{{query_string}}" method="post">
            <input type="submit" value="Choisir cette tâche">
        </form>

        <form action="/todo/{{todolist_name}}/item/{{task_2.key}}/close?{{query_string}}" method="post">
            <input type="submit" value="C'est fait">
        </form>
    </div>
</div>

