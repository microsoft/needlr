from needlr import FabricClient
from needlr.models.workspace import Workspace, WorkspaceRole, GroupPrincipal
from needlr.models.item import ItemType

class TestWorkspaceRoleAssignment:
    def test_workspace_role_assign(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
        res = fc.workspace.role.assign(workspace_id=workspace_test.id, principal=GroupPrincipal(id=testParameters['principal_id']), role=WorkspaceRole.Contributor)
        assert res.is_successful

    def test_workspace_role_ls(self, fc: FabricClient, workspace_test: Workspace):
        res = fc.workspace.role.ls(workspace_id=workspace_test.id)
        # Admin and newly assgined role expected
        assert len(list(res)) == 2

    def test_role_update(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
        res = fc.workspace.role.update(workspace_id=workspace_test.id, principal=GroupPrincipal(id=testParameters['principal_id']), role=WorkspaceRole.Member)
        assert res.is_successful
    
    def test_role_delete(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
        res = fc.workspace.role.delete(workspace_id=workspace_test.id, principal=GroupPrincipal(id=testParameters['principal_id']))
        assert res.is_successful
