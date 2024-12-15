import {useSelector} from "react-redux";
import React from "react";
import {selectNumberOfTasks} from "@/lib/todolist.slice";
import {RootState} from "@/lib/store";

export function TaskCounter() {
    const state = useSelector((root: RootState) => root.todolistPage.numberOfTasks);

    return (<>
        {state.status == "loading" && <div>Il y a ? tâche(s) en cours (Chargement...)</div>}
    </>)
}