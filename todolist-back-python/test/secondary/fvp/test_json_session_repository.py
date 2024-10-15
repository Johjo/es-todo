import json
import os

from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from secondary.fvp.json_session_repository import JsonSessionRepository
from test.secondary.fvp.test_session_repository_contract_testing import TestSessionRepositoryContractTesting


class TestJsonSessionRepository(TestSessionRepositoryContractTesting):
    def feed(self, snapshot: FvpSnapshot) -> None:
        with open(self.path, 'w') as file:
            file.write(json.dumps(snapshot.to_primitive_dict(), indent=4))

    def _create_sut(self) -> FvpSessionSetPort:
        if not os.path.exists('data_test'):
            os.makedirs('data_test')
        self.path = 'data_test/session_fvp.json'

        if os.path.exists(self.path):
            os.remove(self.path)

        return JsonSessionRepository(self.path)




