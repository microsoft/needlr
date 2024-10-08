from typing import Generator
import pytest
from needlr import auth, FabricClient
from needlr.models.datapipeline import Datapipeline
from needlr.models.workspace import Workspace

@pytest.fixture(scope='session')
def datapipeline_test(fc: FabricClient, workspace_test:Workspace, testParameters) -> Generator[Datapipeline, None, None]:
    dp = fc.warehouse.create(display_name=testParameters['datapipeline_name'], workspace_id=workspace_test.id, description=testParameters['datapipeline_description'])
    yield dp