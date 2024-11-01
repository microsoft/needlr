import pytest

from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.eventhouse import Eventhouse

class TestEventhouseLifeCycle:

    def test_eventhouse_ls_and_get(self, fc: FabricClient, workspace_test: Workspace, test_eventhouse:Eventhouse):
        ehs = fc.eventhouse.ls(workspace_id=workspace_test.id)
        for e in ehs:
            eh = fc.eventhouse.get(workspace_id=workspace_test.id, eventhouse_id=e.id)
            assert eh is not None
            break
    
    @pytest.mark.order(after="test_eventhouse_ls_and_get")
    def test_eventhouse_update_definition(self, fc: FabricClient, workspace_test: Workspace, test_eventhouse:Eventhouse, testParameters: dict[str, str]):
        res = fc.eventhouse.update_definition(workspace_id=workspace_test.id, eventhouse_id=test_eventhouse.id, description='New'+testParameters['eventhouse_description'], display_name='New'+testParameters['eventhouse_name'])
        assert type(res) == Eventhouse
    
    @pytest.mark.order(after="test_eventhouse_update_definition")
    def test_eventhouse_clone(self, fc: FabricClient, workspace_test: Workspace, test_eventhouse:Eventhouse):
        cloned = fc.eventhouse.clone(source_workspace_id=workspace_test.id, 
                                        eventhouse_id=test_eventhouse.id, 
                                        clone_name= 'cloned_'+test_eventhouse.name,  
                                        target_workspace_id=workspace_test.id)
        assert type(cloned) == Eventhouse
        
    
