import pytest
from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.kqldashboard import KQLDashboard

class TestKQLDashboardLifeCycle:

    def test_kqlDashboard_ls(self, fc: FabricClient, workspace_test: Workspace, kqlDashboard_test: KQLDashboard):
        kqlDashboard = fc.kqldashboard.ls(workspace_id=workspace_test.id)
        for k in list(kqlDashboard):
            if k.id == kqlDashboard_test.id:
                assert True
                return
    
    @pytest.mark.order(after="test_kqlDashboard_ls")
    def test_kqlDashboard_get(self, fc: FabricClient, workspace_test: Workspace, kqlDashboard_test: KQLDashboard):
        kqlDash = fc.kqldashboard.get(workspace_id=workspace_test.id, kqlDashboard_id=kqlDashboard_test.id)
        assert kqlDash is not None

    @pytest.mark.order(after="test_kqlDashboard_get")
    def test_kqlDashboard_update(self, fc: FabricClient, workspace_test: Workspace, kqlDashboard_test: KQLDashboard, testParameters: dict[str, str]):
        kqlDash = fc.kqldashboard.update(workspace_id=workspace_test.id, kqlDashboard_id=kqlDashboard_test.id, display_name='new'+testParameters['kqlDashboard_displayName'],description='New'+testParameters['kqlDashboard_description'])
        assert type(kqlDash) is KQLDashboard

    @pytest.mark.order(after="test_kqlDashboard_update")
    def test_kqlDashboard_update_definition(self, fc: FabricClient, workspace_test: Workspace, kqlDashboard_test: KQLDashboard, testParameters: dict[str, str]):
        kqlDash = fc.kqldashboard.update_definition(workspace_id=workspace_test.id, kqlDashboard_id=kqlDashboard_test.id, update_metadata=testParameters['kqlDashboard_updateMetadata'], definition=testParameters['kqlDashboard_definition'])
        assert type(kqlDash) is KQLDashboard

    @pytest.mark.order(after="test_kqlDashboard_update_definition")
    def test_kqlDashboard_get_definition(self, fc: FabricClient, workspace_test: Workspace, kqlDashboard_test: KQLDashboard):
        definition = fc.kqldashboard.get_definition(workspace_id=workspace_test.id, kqlDashboard_id=kqlDashboard_test.id)
        assert definition is not None
    
    @pytest.mark.order(after="test_kqlDashboard_get_definition")
    def test_kqlDashboard_delete(self, fc: FabricClient, workspace_test: Workspace, kqlDashboard_test: KQLDashboard):
        kqlDash = fc.kqldashboard.delete(workspace_id=workspace_test.id, kqlDashboard_id=kqlDashboard_test.id)
        assert kqlDash.is_successful is True