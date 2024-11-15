<H2>  Reporter la tâche </H2>
<p>{{ task.name }}</p>

<form action="/todo/{{todolist_name}}/item/{{task.key}}/postpone?{{query_string}}" method="post">
    % for field in form.fields.values():
        <label for="{{ field.name }}">{{ field.label }}</label>
        <input type="date" id="{{ field.name }}" name="{{ field.name }}"
               value="{{ field.value }}">
    % end
    <input type="submit" value="Reporter">
</form>
