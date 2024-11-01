from needlr import FabricClient
from needlr.models.workspace import Workspace

class TestWorkspaceIdentity:
    def test_workspace_provision_identity(self, fc: FabricClient, workspace_test: Workspace):
        res = fc.workspace.identity.provision_identity(workspace_id=workspace_test.id)
        assert res.is_successful

    def test_workspace_deprovision_identity(self, fc: FabricClient, workspace_test: Workspace):
        res = fc.workspace.identity.deprovision_identity(workspace_id=workspace_test.id)
        assert res.is_successful        