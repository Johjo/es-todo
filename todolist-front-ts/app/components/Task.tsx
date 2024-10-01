import React from "react";

interface TaskProps {
    name?: string
}

export function Task({name}: TaskProps) {
    return <div>
        <strong>{name}</strong>
        <button>Renommer</button>
        <button>C'est fait</button>
    </div>;
}