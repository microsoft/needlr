from typing import Generator
import pytest
from needlr import FabricClient
from needlr.models.mlmodel import MLModel
from needlr.models.mlexperiment import MLExperiment

@pytest.fixture(scope='session')
def mlmodel_test(fc: FabricClient, testParameters) -> Generator[MLModel, None, None]:
    mm = fc.mlmodel.create(workspace_id=testParameters['workspace_id'],
                           display_name=testParameters['mlmodel_displayName'],
                           description=testParameters['mlmodel_description'])
    yield mm

@pytest.fixture(scope='session')
def mlexperiment_test(fc: FabricClient, testParameters) -> Generator[MLExperiment, None, None]:
    me = fc.mlexperiment.create(workspace_id=testParameters['workspace_id'],
                                display_name=testParameters['mlexperiment_displayName'],
                                description=testParameters['mlexperiment_description'])
    yield me