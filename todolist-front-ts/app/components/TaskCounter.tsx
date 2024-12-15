import {useSelector} from "react-redux";
import React from "react";
import {RootState} from "@/lib/store";
import {NumberOfTaskLoaded} from "@/lib/todolistPage.slice";

export function TaskCounter() {
    const state = useSelector((root: RootState) => root.todolistPage.numberOfTasks);

    return (<>
        {state.status == "loading" && <NumberOfTasksLoading/>}
        {state.status == "idle" && <NumberOfTasksLoaded state={state}/>}
    </>)
}

function NumberOfTasksLoading() {
    return <div>Il y a ? tâche(s) en cours (Chargement...)</div>;
}

function NumberOfTasksLoaded({state}: { state: NumberOfTaskLoaded }) {
    if (state.numberOfTasks <= 1) {
        return <div>Il y a {state.numberOfTasks} tâche en cours</div>;
    }

    return <div>Il y a {state.numberOfTasks} tâches en cours</div>;
}
