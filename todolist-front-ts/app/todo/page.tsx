"use client";
import React, {useEffect} from "react";
import {TaskCounter} from "@/app/components/TaskCounter";
import {Controller, useDependencies} from "@/app/controller";
import {useAppStore} from "@/lib/hooks";
import {Context} from "@/app/components/Context";
import {WhichTask} from "@/app/components/WhichTask";

function
Todolist() {
    return <>
        <h1>Todolist (construction en cours)</h1>
        <WhichTask/>
        <TaskCounter/>
        <Context/>

        <p>
            <button>Exporter les tâches</button>
            <button>Importer les tâches</button>
        </p>


    </>;
}

function onPageLoad() {
    const store = useAppStore();
    const dependencies = useDependencies();

    useEffect(() => {
        const controller = new Controller(store, dependencies);
        controller.askForWhichTask();

        // controller.refreshTodolist();
    }, [store, dependencies]);
}

export default function IndexPage() {
    onPageLoad();
    return <Todolist/>;
}