% rebase('base.tpl')
<p>
<h2> Importer une tâche</h2>
    <form action="/todo/{{todolist_name}}/import" method="post">
        <textarea rows="10" cols="80" name="markdown_import"></textarea>
        <input type="submit" value="Importer">
    </form>

</p>