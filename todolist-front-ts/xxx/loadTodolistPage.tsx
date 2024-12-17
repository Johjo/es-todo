import {AppDispatch, AppThunk, Dependencies, RootState} from "@/lib/store";
import {NumberOfTasksFetched, TasksContextFetched, WhichTaskFetched} from "@/lib/todolistPage.slice";

type LoadTodolistPageFn = () => any;

export const LoadTodolistPage: LoadTodolistPageFn = (): AppThunk =>
    async (dispatch: AppDispatch, getState: () => RootState, dependencies: Dependencies) => {
        dependencies.whichTasksGateway.get().then((task: any[]) => {
            dispatch(WhichTaskFetched({tasks: task}))
        });


        dependencies.whichTasksGateway.get().then((task: any[]) => {
            dispatch(WhichTaskFetched({tasks: task}))
        });
        dependencies.numberOfTaskGateway.get().then((numberOfTasks: number) => {
            dispatch(NumberOfTasksFetched({numberOfTasks: numberOfTasks}))
        });

        dependencies.contextGateway.get().then((context: string[]) => {
            dispatch(TasksContextFetched({context: context}))
        });
        // dispatch(TasksContextFetched());

    };
