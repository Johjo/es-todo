% rebase('base.tpl')
<div class="choose-task">
    <div class="main-task">
        % include('task_title', task_name=name_1, task_id=index_1, task=task_1)
        <form action="/todo/{{todolist_name}}/item/choose/{{index_1}}/ignore/{{index_2}}?{{query_string}}" method="post">
            <input type="submit" value="Choisir cette tâche">
        </form>

        % include('cancel_priority_button', task_key=index_1)

        <form action="/todo/{{todolist_name}}/item/{{index_1}}/close?{{query_string}}" method="post">
            <input type="submit" value="C'est fait">
        </form>
    </div>

    <div class="secondary-task">
        % include('task_title', task_name=name_2, task_id=index_2, task=task_2)
        <form action="/todo/{{todolist_name}}/item/choose/{{index_2}}/ignore/{{index_1}}?{{query_string}}" method="post">
            <input type="submit" value="Choisir cette tâche">
        </form>

        <form action="/todo/{{todolist_name}}/item/{{index_2}}/close?{{query_string}}" method="post">
            <input type="submit" value="C'est fait">
        </form>
    </div>
</div>

