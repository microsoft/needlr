import pytest
from needlr import auth, FabricClient
from needlr.models.warehouse import Warehouse
from needlr.models.workspace import Workspace

@pytest.fixture(scope='session')
def warehouse_test(fc: FabricClient, workspace_test:Workspace, testParameters):
    ws = fc.warehouse.create(display_name=testParameters['warehouse_name'], workspace_id=workspace_test.id, description=testParameters['warehouse_description'])
    yield ws