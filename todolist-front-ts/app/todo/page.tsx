"use client";
import React from "react";
import {TaskCounter} from "@/app/components/TaskCounter";
import {Context} from "@/app/components/Context";
import {WhichTask} from "@/app/components/WhichTask";
import {AppStore} from "@/lib/store";
import {useAppStore} from "@/lib/hooks";
import {LoadTodolistPage} from "@/xxx/loadTodolistPage";

function
Todolist() {
    return <>
        <h1>Todolist</h1>
        <WhichTask/>
        <TaskCounter/>
        <Context/>
        <p>
            <button>Exporter les tâches</button>
            <button>Importer les tâches</button>
        </p>
    </>;
}

export default function IndexPage() {
    const store: AppStore = useAppStore();
    store.dispatch(LoadTodolistPage())
    return <Todolist/>;
}