from typing import Generator
import pytest
from needlr import FabricClient
from needlr.models.mlmodel import MLModel

@pytest.fixture(scope='session')
def mlmodel_test(fc: FabricClient, testParameters) -> Generator[MLModel, None, None]:
    mm = fc.mlmodel.create(workspace_id=testParameters['workspace_id'],
                           display_name=testParameters['workspace_name'],
                           description=testParameters['description'])
    yield mm