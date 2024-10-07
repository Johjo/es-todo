"use client";
import React, {useEffect} from "react";
import {TaskCounter} from "@/app/components/TaskCounter";
import {useDependencies} from "@/app/dependenciesProvider";
import {useAppStore} from "@/lib/hooks";
import {Context} from "@/app/components/Context";
import {WhichTask} from "@/app/components/WhichTask";
import {Controller} from "@/primary/controller/whichTask";
import {AppStore} from "@/lib/store";
import {StoreContract} from "@/primary/controller/chooseAndIgnoreTask";

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

class StoreForController implements StoreContract {
    constructor(private readonly store: AppStore) {

    }

    dispatch(event: any): void {
        this.store.dispatch(event);
    }
}

function onPageLoad() {
    const store: AppStore = useAppStore();
    const dependencies = useDependencies();

    useEffect(() => {
        const controller = new Controller({...dependencies}, new StoreForController(store));
        controller.execute();
    }, [store, dependencies]);
}

export default function IndexPage() {
    onPageLoad();
    return <Todolist/>;
}