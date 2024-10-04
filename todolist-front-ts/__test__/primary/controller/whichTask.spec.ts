import {WhichTask} from "@/hexagon/whichTask.query";
import {DependencyList, StoreContract, Toto} from "@/primary/controller/chooseAndIgnoreTask";
import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";


class DependencyListForTest implements DependencyList {
    whichTaskQuery(): WhichTask.Contract {
        throw new Error("Method not implemented.");
    }

    store(): StoreContract {
        throw new Error("Method not implemented.");
    }

    chooseAndIgnoreTaskUseCase(): ChooseAndIgnoreTask.Contract {
        throw new Error("Method not implemented.");
    }
}


describe('controller', () => {
    it.skip('should dispatch whichTaskUpdated', () => {
        const sut = new Toto.Controller(new DependencyListForTest());
        sut.refreshWhichTask()
    })
});