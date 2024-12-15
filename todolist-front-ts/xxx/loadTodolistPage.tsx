import {AppDispatch, RootState} from "@/lib/store";
import {NumberOfTasksFetched, TasksContextFetched, WhichTaskFetched} from "@/lib/todolistPage.slice";

export function LoadTodolistPage() {
    return (dispatch: AppDispatch, getState: () => RootState) => {
        dispatch(WhichTaskFetched({tasks: []}));
        dispatch(TasksContextFetched());
        dispatch(NumberOfTasksFetched());

    }
}