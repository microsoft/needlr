from needlr import FabricClient
from needlr.models.workspace import Workspace

class TestDatamartLifeCycle:

    def test_datamart_ls(self, fc: FabricClient, workspace_test: Workspace):
        dm = fc.datamartclient.ls(workspace_id=workspace_test.id)
        assert len(list(dm)) == 0 # No Datamarts created yet