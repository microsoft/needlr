from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.semanticmodel import SemanticModel

import pytest

class TestSemanticModelLifeCycle:

    @pytest.mark.skip(reason="Waiting for actual implementation")
    @pytest.fixture
    def test_semanticmodel(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
        sm = fc.semanticmodel.create(workspace_id=workspace_test.id, display_name=testParameters['semanticmodel_name'])
        assert sm.name == testParameters['semanticmodel_name']

    @pytest.mark.skip(reason="Waiting for create to work")
    def test_semanticmodel_ls(self, fc: FabricClient, workspace_test: Workspace):
        sm = fc.semanticmodel.ls(workspace_id=workspace_test.id)
        assert len(list(sm)) == 1

    @pytest.mark.skip(reason="Waiting for actual implementation")
    def test_semanticmodel_update(self, fc: FabricClient, workspace_test: Workspace, test_semanticmodel:SemanticModel, testParameters: dict[str, str]):
        sm = fc.semanticmodel.update(workspace_id=workspace_test.id, semanticmodel_id=test_semanticmodel.id, display_name='New'+ testParameters['semanticmodel_name'])
        assert sm.name == 'New'+ testParameters['semanticmodel_name']

    @pytest.mark.skip(reason="Waiting for actual implementation")
    def test_semanticmodel_get(self, fc: FabricClient, workspace_test: Workspace, test_semanticmodel:SemanticModel, testParameters: dict[str, str]):
        sm = fc.semanticmodel.get(workspace_id=workspace_test.id, semanticmodel_id=test_semanticmodel.id)
        assert sm.id == test_semanticmodel.id and sm.name == 'New'+ testParameters['semanticmodel_name']

    @pytest.mark.skip(reason="Waiting for create to work")
    def test_semanticmodel_delete(self, fc: FabricClient, workspace_test: Workspace, test_semanticmodel:SemanticModel):
        resp = fc.semanticmodel.delete(workspace_id=workspace_test.id, semanticmodel_id=test_semanticmodel.id)
        assert resp.is_successful is True