import pytest
from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.mlexperiment import MLExperiment

class TestMLExperimentLifeCycle:

    def test_mlexperiment_ls(self, fc: FabricClient, workspace_test: Workspace, mlexperiment_test: MLExperiment):
        me = fc.mlexperiment.ls(workspace_id=workspace_test.id)
        for m in list(me):
            if m.id == mlexperiment_test.id:
                assert True
                return
            
    @pytest.mark.order(after="test_mlexperiment_ls")
    def test_mlexperiment_get(self, fc: FabricClient, workspace_test: Workspace, mlexperiment_test: MLExperiment):
        me = fc.mlexperiment.get(workspace_id=workspace_test.id, mlexperiment_id=mlexperiment_test.id)
        assert me is not None

    @pytest.mark.order(after="test_mlexperiment_get")
    def test_mlexperiment_update_definition(self, fc: FabricClient, workspace_test: Workspace, mlexperiment_test: MLExperiment):
        me = fc.mlexperiment.update(workspace_id=workspace_test.id, mlexperiment_id=mlexperiment_test.id)
        assert type(me) is MLExperiment
    
    @pytest.mark.order(after="test_mlexperiment_delete")
    def test_mlexperiment_delete(self, fc: FabricClient, workspace_test: Workspace, mlexperiment_test: MLExperiment):
        resp = fc.mlexperiment.delete(workspace_id=workspace_test.id, mlexperiment_id=mlexperiment_test.id)
        assert resp.is_successful is True