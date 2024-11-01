import pytest

from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.notebook import Notebook

class TestNotebook:

    def test_notebook_ls(self, fc: FabricClient, workspace_test: Workspace, notebook_test:Notebook):
        int_nb = notebook_test
        notebooks = fc.notebook.ls(workspace_id=workspace_test.id)
        assert len(list(notebooks)) > 0

    @pytest.mark.order(after="test_notebook_ls")
    def test_notebook_get(self, fc: FabricClient, workspace_test: Workspace, notebook_test: Notebook):
        nb = fc.notebook.get(workspace_id=workspace_test.id, notebook_id=notebook_test.id)
        assert type(nb) is Notebook

    @pytest.mark.order(after="test_notebook_get")
    def test_notebook_update(self, fc: FabricClient, workspace_test: Workspace, notebook_test: Notebook,testParameters: dict[str, str]):
        nb = fc.notebook.update(workspace_id=workspace_test.id, notebook_id=notebook_test.id, display_name='new'+testParameters['notebook_name'], description='New'+testParameters['notebook_description'])
        assert type(nb) is Notebook    

    @pytest.mark.order(after="test_notebook_update")
    def test_notebook_delete(self, fc: FabricClient, workspace_test: Workspace, notebook_test: Notebook):
        resp = fc.notebook.delete(workspace_id=workspace_test.id, notebook_id=notebook_test.id)
        assert resp.is_successful is True            