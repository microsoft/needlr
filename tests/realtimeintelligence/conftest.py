import pytest
from needlr import auth, FabricClient
from needlr.models.eventstream import Eventstream
from needlr.models.workspace import Workspace
import pickle

@pytest.fixture(scope='session')
def test_eventstream(fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
    new_name='New'+testParameters['eventstream_name']
    new_description='New'+testParameters['eventstream_description']
    es = fc.eventstream.create(workspace_id=workspace_test.id, display_name=new_name, description=new_description)
    yield es