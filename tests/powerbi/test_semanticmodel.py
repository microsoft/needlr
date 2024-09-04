from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.semanticmodel import SemanticModel

import pytest

class TestSemanticModelLifeCycle:

    def test_semanticmodel_ls(self, fc: FabricClient, workspace_test: Workspace, test_semanticmodel:SemanticModel):
        sm = fc.semanticmodel.ls(workspace_id=workspace_test.id)
        for s in list(sm):
            if s.id == test_semanticmodel.id:
                assert True
                return

    def test_semanticmodel_get(self, fc: FabricClient, workspace_test: Workspace, test_semanticmodel:SemanticModel):
        sm = fc.semanticmodel.get(workspace_id=workspace_test.id, semanticmodel_id=test_semanticmodel.id)
        assert sm is not None

    def test_semanticmodel_update_definition(self, fc: FabricClient, workspace_test: Workspace, test_semanticmodel:SemanticModel, sm_definition:dict):
        res = fc.semanticmodel.update_definition(workspace_id=workspace_test.id, semanticmodel_id=test_semanticmodel.id, definition=sm_definition)
        assert res.is_successful is True

    def test_semanticmodel_get_definition(self, fc: FabricClient, workspace_test: Workspace, test_semanticmodel:SemanticModel):
        definition = fc.semanticmodel.get_definition(workspace_id=workspace_test.id, semanticmodel_id=test_semanticmodel.id)
        assert definition['parts'] is not None

    def test_semantic_model_clone(self, fc: FabricClient, workspace_test: Workspace, test_semanticmodel:SemanticModel):
        cloned = fc.semanticmodel.clone(workspace_id=workspace_test.id, semanticmodel_id=test_semanticmodel.id, clone_name=f'{test_semanticmodel.name}_cloned')
        assert cloned is not None
        if cloned is not None:
            fc.semanticmodel.delete(workspace_id=workspace_test.id, semanticmodel_id=cloned.id)    

    def test_semanticmodel_delete(self, fc: FabricClient, workspace_test: Workspace, test_semanticmodel:SemanticModel):
        resp = fc.semanticmodel.delete(workspace_id=workspace_test.id, semanticmodel_id=test_semanticmodel.id)
        assert resp.is_successful is True
        
        
    
