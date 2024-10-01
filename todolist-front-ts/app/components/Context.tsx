import {useSelector} from "react-redux";
import {RootState} from "@/lib/store";
import React from "react";

export function Context() {
    const contexts = useSelector((root: RootState) => root.todolist.contexts);
    return <div>
        <h2>Contexte</h2>
        <ul>
            <li>Inbox</li>
            {contexts.map((context) => <li key={context}>{context}</li>)}
            <li>All</li>
        </ul>
    </div>;
}