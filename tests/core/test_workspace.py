from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.item import ItemType

class TestWorkspaceLifeCycle:
    def test_workspace_get(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
        ws = fc.workspace.get(workspace_id=workspace_test.id)
        assert ws.name == testParameters['workspace_name']

    def test_workspace_update(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
        ws = fc.workspace.update(workspace_id=workspace_test.id, display_name='New'+ workspace_test.name)
        assert ws.name == 'New'+ testParameters['workspace_name']

    def test_workspace_capacity_unassign(self, fc: FabricClient, workspace_test: Workspace):
        ws = fc.workspace.capacity_unassign(workspace_id=workspace_test.id)
        assert ws.is_successful is True

    def test_workspace_capacity_assign(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
        ws = fc.workspace.capacity_assign(workspace_id=workspace_test.id, capacity_id=testParameters['capacity_id'])
        assert ws.is_successful is True

    def test_workspace_item_ls(self, fc: FabricClient, workspace_test: Workspace):
        items = fc.workspace.item_ls(workspace_id=workspace_test.id)
        assert len(list(items)) == 0

    def test_wokspace_item_ls_with_type(self, fc: FabricClient, workspace_test: Workspace):
        items = fc.workspace.item_ls(workspace_id=workspace_test.id, item_type=ItemType.DataPipeline)
        assert len(list(items)) == 0