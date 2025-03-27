import pytest
from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.mlmodel import MLModel

class TestMLModelLifeCycle:

    def test_mlmodel_ls(self, fc: FabricClient, workspace_test: Workspace, mlmodel_test: MLModel):
        mm = fc.mlmodel.ls(workspace_id=workspace_test.id)
        for m in list(mm):
            if m.id == mlmodel_test.id:
                assert True
                return
            
    @pytest.mark.order(after="test_mlmodel_ls")
    def test_mlmodel_get(self, fc: FabricClient, workspace_test: Workspace, mlmodel_test: MLModel):
        mm = fc.mlmodel.get(workspace_id=workspace_test.id, mlmodel_id=mlmodel_test.id)
        assert mm is not None

    @pytest.mark.order(after="test_mlmodel_get")
    def test_mlmodel_update_definition(self, fc: FabricClient, workspace_test: Workspace, mlmodel_test: MLModel):
        mm = fc.mlmodel.update(workspace_id=workspace_test.id, mlmodel_id=mlmodel_test.id)
        assert type(mm) is MLModel
    
    @pytest.mark.order(after="test_mlmodel_delete")
    def test_mlmodel_delete(self, fc: FabricClient, workspace_test: Workspace, mlmodel_test: MLModel):
        resp = fc.mlmodel.delete(workspace_id=workspace_test.id, mlmodel_id=mlmodel_test.id)
        assert resp.is_successful is True