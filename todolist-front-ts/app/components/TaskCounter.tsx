import {useSelector} from "react-redux";
import React from "react";
import {selectNumberOfTasks} from "@/lib/todolist.slice";

export function TaskCounter() {
    const numberOfTasks = useSelector(selectNumberOfTasks);

    console.log(numberOfTasks)
    if (numberOfTasks > 1) {
        return <div>Il y a {numberOfTasks} tâches en cours</div>;
    }

    return <div>Il y a {numberOfTasks} tâche en cours</div>;
}