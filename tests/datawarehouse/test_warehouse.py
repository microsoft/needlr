from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.warehouse import Warehouse

import pytest

class TestWarehouseLifeCycle:

    def test_warehouse_ls(self, fc: FabricClient, workspace_test: Workspace, warehouse_test: Warehouse):
        # t = warehouse_test
        whs = fc.warehouse.ls(workspace_id=workspace_test.id)
        assert len(list(whs)) == 1

    def test_warehouse_update(self, fc: FabricClient, workspace_test: Workspace, warehouse_test:Warehouse, testParameters: dict[str, str]):
        wh = fc.warehouse.update(workspace_id=workspace_test.id, warehouse_id=warehouse_test.id, display_name='New'+ testParameters['warehouse_name'])
        assert wh.name == 'New'+ testParameters['warehouse_name']

    def test_warehouse_get(self, fc: FabricClient, workspace_test: Workspace, warehouse_test:Warehouse , testParameters: dict[str, str]):
        wh = fc.warehouse.get(workspace_id=workspace_test.id, warehouse_id=warehouse_test.id)
        assert wh.id == warehouse_test.id and wh.name == 'New'+ testParameters['warehouse_name']

    def test_warehouse_delete(self, fc: FabricClient, workspace_test: Workspace, warehouse_test:Warehouse):
        resp = fc.warehouse.delete(workspace_id=workspace_test.id, warehouse_id=warehouse_test.id)
        assert resp.is_successful is True