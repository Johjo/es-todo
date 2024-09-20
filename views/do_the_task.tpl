% rebase('base.tpl')
<p>
    <h2> {{task_name}} </h2>
    <form action="/todo/{{todolist_name}}/item/{{task_id}}/close" method="post">
    <input type="submit" value="C'est fait">
    </form>
</p>

