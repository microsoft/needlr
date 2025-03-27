import pytest
from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.reflex import Reflex

class TestReflexLifeCycle:

    def test_reflex_ls(self, fc: FabricClient, workspace_test: Workspace, reflex_test: Reflex):
        ref = fc.reflex.ls(workspace_id=workspace_test.id)
        for r in list(ref):
            if r.id == reflex_test.id:
                assert True
                return
    
    @pytest.mark.order(after="test_reflex_ls")
    def test_reflex_get(self, fc: FabricClient, workspace_test: Workspace, reflex_test: Reflex):
        ref = fc.reflex.get(workspace_id=workspace_test.id, reflex_id=reflex_test.id)
        assert ref is not None

    @pytest.mark.order(after="test_reflex_get")
    def test_reflex_update(self, fc: FabricClient, workspace_test: Workspace, reflex_test: Reflex, testParameters: dict[str, str]):
        ref = fc.reflex.update(workspace_id=workspace_test.id, reflex_id=reflex_test.id, display_name='new'+testParameters['reflex_displayName'],description='New'+testParameters['reflex_description'])
        assert type(ref) is Reflex

    @pytest.mark.order(after="test_reflex_update")
    def test_reflex_update_definition(self, fc: FabricClient, workspace_test: Workspace, reflex_test: Reflex, testParameters: dict[str, str]):
        ref = fc.reflex.update_definition(workspace_id=workspace_test.id, reflex_id=reflex_test.id, update_metadata=testParameters['reflex_updateMetadata'], definition=testParameters['reflex_definition'])
        assert type(ref) is Reflex

    @pytest.mark.order(after="test_reflex_update_definition")
    def test_reflex_get_definition(self, fc: FabricClient, workspace_test: Workspace, reflex_test: Reflex):
        definition = fc.reflex.get_definition(workspace_id=workspace_test.id, reflex_id=reflex_test.id)
        assert definition is not None
    
    @pytest.mark.order(after="test_reflex_get_definition")
    def test_reflex_delete(self, fc: FabricClient, workspace_test: Workspace, reflex_test: Reflex):
        ref = fc.reflex.delete(workspace_id=workspace_test.id, reflex_id=reflex_test.id)
        assert ref.is_successful is True