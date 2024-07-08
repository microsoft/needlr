import pytest
from needlr import auth, FabricClient
from needlr.models.warehouse import Warehouse
from needlr.models.workspace import Workspace

@pytest.mark.skip(reason="waiting for long-running warehouse.create implementation")
@pytest.fixture(scope='session')
def warehouse_test(fc: FabricClient, workspace:Workspace, testParameters) -> Warehouse:
    ws = fc.warehouse.create(display_name=testParameters['warehouse_name'], workspace_id=workspace.id, description=testParameters['warehouse_description'])
    yield ws