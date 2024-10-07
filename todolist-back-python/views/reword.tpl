<form action="/todo/{{todolist_name}}/item/{{task_id}}/reword?{{query_string}}" method="post">
    <input type="text" name="new_name" value="{{task_name}}">
    <input type="submit" value="Renommer">
</form>
