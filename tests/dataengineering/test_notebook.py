import pytest
import uuid
import base64

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
    def test_notebook_update_definition(self, fc: FabricClient, workspace_test: Workspace, notebook_test: Notebook):
        nb = fc.notebook.update_definition(workspace_id=workspace_test.id, notebook_id=notebook_test.id, definition={
             "definition": {
                "parts": [
                    {
                        "path": "notebook-content.py",
                        "payload": base64.b64encode(open('tests/dataengineering/notebook_test_part0.txt', 'rb').read()).decode('utf-8'),
                        "payloadType": "InlineBase64"
                    },
                    {
                        "path": ".platform",
                        "payload": base64.b64encode(open('tests/dataengineering/notebook_test_part1.txt', 'rb').read()).decode('utf-8'),
                        "payloadType": "InlineBase64"
                    }
                ]
            }
        })
        assert type(nb) is Notebook    
    
    @pytest.mark.order(after="test_notebook_update_definition")
    def test_notebook_get_definition(self, fc: FabricClient, workspace_test: Workspace, notebook_test: Notebook):
        definition = fc.notebook.get_definition(workspace_id=workspace_test.id, notebook_id=notebook_test.id)
        assert definition is not None

    @pytest.mark.order(after="test_notebook_get_definition")
    def test_update_default_lakehouse(self, fc: FabricClient, workspace_test: Workspace, notebook_test: Notebook):
        nb = fc.notebook.update_default_lakehouse(workspace_id=workspace_test.id, notebook_id=notebook_test.id, default_lakehouse_id=uuid.uuid4(), default_lakehouse_name="MY_NEW_NAME")
        assert nb is not None

    @pytest.mark.order(after="test_update_default_lakehouse")
    def test_notebook_delete(self, fc: FabricClient, workspace_test: Workspace, notebook_test: Notebook):
        resp = fc.notebook.delete(workspace_id=workspace_test.id, notebook_id=notebook_test.id)
        assert resp.is_successful is True            