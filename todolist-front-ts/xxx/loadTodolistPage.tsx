import {AppDispatch, AppThunk, Dependencies, RootState} from "@/lib/store";
import {NumberOfTasksFetched, TasksContextFetched, WhichTaskFetched} from "@/lib/todolistPage.slice";

type LoadTodolistPageFn = () => any;

export const LoadTodolistPage: LoadTodolistPageFn = (): AppThunk =>
    async (dispatch: AppDispatch, getState: () => RootState, dependencies: Dependencies) => {
        dependencies.whichTasksGateway.get().then(() => {dispatch(WhichTaskFetched({tasks: []}))});

        dispatch(TasksContextFetched());
        dispatch(NumberOfTasksFetched({numberOfTasks: 0}));
    };
