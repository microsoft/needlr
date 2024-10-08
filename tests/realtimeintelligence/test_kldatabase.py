import pytest

from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.kqldatabase import KQLDatabase

class TestKQLDatabaseLifeCycle:

    def test_kqlDatabase_ls(self, fc: FabricClient, workspace_test: Workspace, test_kqlDatabase: KQLDatabase):
        t = test_kqlDatabase
        kqldbs = fc.kqldatabase.ls(workspace_id=workspace_test.id)
        assert len(list(kqldbs)) > 0

    @pytest.mark.order(after="test_kqlDatabase_ls")
    def test_kqlDatabase_get(self, fc: FabricClient, workspace_test: Workspace, test_kqlDatabase: KQLDatabase):
        a = workspace_test.id
        b = test_kqlDatabase.id
        kqldbs = fc.kqldatabase.get(workspace_id=workspace_test.id, kqlDatabase_id=test_kqlDatabase.id)
        assert type(kqldbs) is KQLDatabase

    @pytest.mark.order(after="test_kqlDatabase_get")
    def test_kqlDatabase_update(self, fc: FabricClient, workspace_test: Workspace, test_kqlDatabase: KQLDatabase,testParameters: dict[str, str]):
        kqldbs = fc.kqldatabase.update(workspace_id=workspace_test.id, kqlDatabase_id=test_kqlDatabase.id, display_name='new'+testParameters['kqlDatabase_name'], description='New'+testParameters['kqlDatabase_description'])
        assert type(kqldbs) is KQLDatabase

    @pytest.mark.order(after="test_kqlDatabase_update")
    def test_kqlDatabase_delete(self, fc: FabricClient, workspace_test: Workspace, test_kqlDatabase: KQLDatabase):
        resp = fc.kqldatabase.delete(workspace_id=workspace_test.id, kqlDatabase_id=test_kqlDatabase.id)
        assert resp.is_successful is True
        
        
    
