import {AppDispatch, makeStore, RootState} from "@/lib/store";

export function LoadTodolistPage() {
    return (dispatch: AppDispatch, getState: () => RootState) => {

    }
}


describe('LoadTodolistPage', () => {
    it('should display todolist page loading when do nothing', async () => {
        // GIVEN
        const store = makeStore();
        const {todolistPage: todolistPageInitialState, ...otherInitialState} = store.getState();

        // WHEN

        // THEN
        const {todolistPage, ...otherState} = store.getState();
        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual({
            fvpTasks: {status: "loading"},
            tasksContext: {status: "loading"},
            numberOfTasks: {status: "loading"},
        });
    });
});