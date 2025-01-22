import pytest
from typing import Generator
from needlr.models.notebook import Notebook
from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.lakehouse import Lakehouse

@pytest.fixture(scope='session')
def notebook_test(fc: FabricClient, workspace_test: Workspace, testParameters) -> Generator[Notebook, None, None]:
    nb = fc.notebook.create(display_name=testParameters['notebook_name'], 
                            workspace_id=workspace_test.id, 
                            description=testParameters['notebook_description'])
    yield nb

@pytest.fixture(scope='session')
def lakehouse_test(fc: FabricClient, workspace_test:Workspace, testParameters) -> Generator[Lakehouse, None, None]:
    lh = fc.lakehouse.create(display_name=testParameters['lakehouse_name'], 
                            workspace_id=workspace_test.id, 
                            description=testParameters['lakehouse_description'], 
                            enableSchemas=True)
    yield lh