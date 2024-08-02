import pytest

from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.eventhouse import Eventhouse

class TestEventhouseLifeCycle:

    def test_eventhouse_create(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
        res = fc.eventhouse.create(workspace_id=workspace_test.id, display_name=testParameters['eventhouse_name'])
        assert res is not None

    @pytest.mark.order(after="test_eventhouse_create")
    def test_eventhouse_ls_and_get(self, fc: FabricClient, workspace_test: Workspace):
        ehs = fc.eventhouse.ls(workspace_id=workspace_test.id)
        for e in ehs:
            eh = fc.eventhouse.get(workspace_id=workspace_test.id, eventhouse_id=e.id)
            assert eh is not None
            break
    
    @pytest.mark.order(after="test_eventhouse_ls_and_get")
    def test_eventhouse_update_definition(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
        ehs = fc.eventhouse.ls(workspace_id=workspace_test.id)
        for e in ehs:
            res = fc.eventhouse.update_definition(workspace_id=workspace_test.id, eventhouse_id=e.id, description='New'+testParameters['eventhouse_description'], display_name='New'+testParameters['eventhouse_name'])
            assert res is not None
            break
    
    @pytest.mark.order(after="test_eventhouse_update_definition")
    def test_eventhouse_clone(self, fc: FabricClient, workspace_test: Workspace):
        ehs = fc.eventhouse.ls(workspace_id=workspace_test.id)
        for e in ehs:
            cloned = fc.eventhouse.clone(source_workspace_id=workspace_test.id, 
                                         eventhouse_id=e.id, 
                                         clone_name= 'str'+e.name,  
                                         target_workspace_id=workspace_test.id)
            assert cloned is not None
            break
    
    @pytest.mark.order(after="test_eventhouse_clone")
    def test_eventhouse_delete(self, fc: FabricClient, workspace_test: Workspace):
        ehs = fc.eventhouse.ls(workspace_id=workspace_test.id)
        for e in ehs:
            resp = fc.eventhouse.delete(workspace_id=workspace_test.id, eventhouse_id=e.id)
            assert resp.is_successful is True
        
        
    
