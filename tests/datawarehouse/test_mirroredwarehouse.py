from needlr import FabricClient
from needlr.models.workspace import Workspace

class TestMirroredWarehouseLifeCycle:

    def test_mirroredwarehouse_ls(self, fc: FabricClient, workspace_test: Workspace):
        whs = fc.mirroredwarehouse.ls(workspace_id=workspace_test.id)
        assert len(list(whs)) == 0