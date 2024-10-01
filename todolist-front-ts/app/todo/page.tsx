"use client";
import React, {useEffect} from "react";
import {TaskCounter} from "@/app/components/TaskCounter";
import {Controller, useDependencies} from "@/app/controller";
import {useAppStore} from "@/lib/hooks";
import {Context} from "@/app/components/Context";

function
Todolist() {
    return <>
        <h1>Todolist (construction en cours)</h1>
        <p>
            <strong>Tâche courante</strong>
            <button>Renommer</button>
            <button>C'est fait</button>
        </p>
        <button>Choisir cette tâche</button>
        <p>
            <strong>Tâche secondaire</strong>
            <button>Renommer</button>
            <button>C'est fait</button>
        </p>
        <button>Choisir cette tâche</button>

        <div><TaskCounter/></div>


        <h2>Contexte</h2>
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
        controller.refreshTodolist();

        // controller.refreshTodolist();
    }, [store, dependencies]);
}

export default function IndexPage() {
    onPageLoad();
    return <Todolist/>;
}