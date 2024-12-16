import {useSelector} from "react-redux";
import {RootState} from "@/lib/store";
import React from "react";
import {WhichTasksLoaded} from "@/lib/todolistPage.slice";


export function WhichTask() {
    const state = useSelector((root: RootState) => root.todolistPage.whichTasks);

    return (<>
        {state.status == "loading" && <WhichTaskLoading></WhichTaskLoading>}
        {state.status == "idle" && <WhichTaskLoaded state={state}></WhichTaskLoaded>}
    </>)
}

function WhichTaskLoading() {
    return <div>Chargement des tâches...</div>;
}

function WhichTaskLoaded(props: { state: WhichTasksLoaded }) {
    return <>
        {props.state.type == "nothing to do" && <NoTask />}
        {props.state.type == "only one task" && <OneTask />}
        {props.state.type == "two tasks" && <TwoTasks />}
    </>;
}

function NoTask() {
    return <div>Rien à faire</div>;
}

function OneTask() {
    return <div>Buy the milk</div>;
}

function TwoTasks() {
    return <>
        <div>Buy the milk</div>
        <div>Buy the water</div>
    </>;
}
