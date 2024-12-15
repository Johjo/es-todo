import {useSelector} from "react-redux";
import {RootState} from "@/lib/store";
import {Task} from "@/app/components/Task";
import React from "react";

export function WhichTask() {
    const state = useSelector((root: RootState) => root.todolistPage.whichTasks);

    return (<>
        {state.status == "loading" && <div>Chargement des tâches...</div>}
    </>)
}