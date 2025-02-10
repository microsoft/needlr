import pytest
from typing import Generator
from needlr.models.notebook import Notebook
from needlr import FabricClient
from needlr.models.workspace import Workspace

@pytest.fixture(scope='session')
def notebook_test(fc: FabricClient, workspace_test: Workspace, testParameters) -> Generator[Notebook, None, None]:
    nb = fc.notebook.create(display_name=testParameters['notebook_name'], 
                            workspace_id=workspace_test.id, 
                            description=testParameters['notebook_description'])
    yield nb

