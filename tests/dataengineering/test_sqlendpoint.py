from needlr import FabricClient
from needlr.models.workspace import Workspace

class TestSQLEndPointLifeCycle:

    def test_sqlendpoint_ls(self, fc: FabricClient, workspace_test: Workspace):
        whs = fc.sqlendpoint.ls(workspace_id=workspace_test.id)
        assert len(list(whs)) == 0 # Only LH have SQL Endpoints