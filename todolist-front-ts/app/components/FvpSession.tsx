import {useSelector} from "react-redux";
import {RootState} from "@/lib/store";
import {Task} from "@/app/components/Task";
import React from "react";

export function FvpSession() {
    const tasks = useSelector((root: RootState) => root.todolist.tasks);
    if (tasks.length === 0) {
        return <>Rien à faire</>;
    }

    if (tasks.length === 1) {
        return <Task name={tasks[0].name}/>;
    }

    return <>
        <div>
            <Task name={tasks[0].name}/>
            <button>Choisir cette tâche</button>
        </div>
        <div>
            <Task name={tasks[1].name}/>
            <button>Choisir cette tâche</button>
        </div>
    </>;
}