import {Task, TodolistPort} from "@/hexagon/whichTaskQuery/whichTask.query";


export function build(): TodolistPort {
    return new TodolistFromApi()
}

export class TodolistFromApi implements TodolistPort {
    async whichTask(): Promise<Task[]> {
        const response: Response = await fetch("http://127.0.0.1:8090/rest/todo/Jonathan/which_task");

        const data = await response.json();
        return data.fvpTasks;
    }
}
