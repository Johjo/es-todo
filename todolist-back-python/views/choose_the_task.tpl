% rebase('base.tpl')
<p>
% include('task_title', task_name=name_1, task_id=index_1)
<form action="/todo/{{todolist_name}}/item/choose/{{index_1}}/ignore/{{index_2}}" method="post">
    <input type="submit" value="Choisir cette tâche">
    <input type="hidden" name="redirect" value="{{url}}">
</form>

<form action="/todo/{{todolist_name}}/item/{{index_1}}/close" method="post">
    <input type="submit" value="C'est fait">
</form>
</p>

<p>
% include('task_title', task_name=name_2, task_id=index_2)
<form action="/todo/{{todolist_name}}/item/choose/{{index_2}}/ignore/{{index_1}}" method="post">
    <input type="submit" value="Choisir cette tâche">
    <input type="hidden" name="redirect" value="{{url}}">
</form>

<form action="/todo/{{todolist_name}}/item/{{index_2}}/close" method="post">
    <input type="submit" value="C'est fait">
</form>
</p>


