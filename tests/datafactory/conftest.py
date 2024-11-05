from typing import Generator
import pytest
import pickle
from needlr import auth, FabricClient
from needlr.models.datapipeline import Datapipeline
from needlr.models.workspace import Workspace

@pytest.fixture(scope='session')
def datapipeline_definition():
    with open('tests/datafactory/datapipeline_definition.pkl', 'rb') as sample_datapipeline_definition:
        definition = pickle.load(sample_datapipeline_definition)
        yield definition

@pytest.fixture(scope='session')
def test_datapipeline(fc: FabricClient, workspace_test:Workspace, datapipeline_definition:dict, testParameters: dict[str, str]) -> Generator[Datapipeline, None, None]:
    dp = fc.datapipeline.create(display_name=testParameters['datapipeline_name'], workspace_id=workspace_test.id,
                                definition=datapipeline_definition, description=testParameters['datapipeline_description'])
    yield dp