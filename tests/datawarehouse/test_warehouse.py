from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.warehouse import Warehouse
from needlr.models.item import ItemType

class TestWarehouseLifeCycle:
    def test_workspace_create(self, fc: FabricClient, workspace: Workspace, testParameters: dict[str, str]):
        wh = fc.warehouse.create(display_name=testParameters['warehouse_name'], workspace_id=workspace.id, description=testParameters['warehouse_description'])
        assert wh.name == testParameters['warehouse_name']
