export namespace ChooseAndIgnoreTask {
    export class UseCase implements Contract {
        constructor(private readonly todolist: Port.Todolist) {

        }

        execute(chosenTaskId: number, ignoredTaskId: number) {
            this.todolist.chooseAndIgnoreTask(chosenTaskId, ignoredTaskId)
        }
    }

    export interface Contract {
        execute(chosenTaskId: number, ignoredTaskId: number): void;
    }

    export namespace Port {
        export interface Todolist {
            chooseAndIgnoreTask(chosenTaskId: number, ignoredTaskId: number): void;
        }

    }


}
