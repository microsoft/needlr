from typing import Generator
import pytest
from needlr import auth, FabricClient
from needlr.models.eventstream import Eventstream
from needlr.models.kqldatabase import KQLDatabase
from needlr.models.eventhouse import Eventhouse
from needlr.models.workspace import Workspace
from needlr.models.kqldashboard import KQLDashboard
import pickle

@pytest.fixture(scope='session')
def test_eventstream(fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]) -> Generator[Eventstream, None, None]:
    es = fc.eventstream.create(workspace_id=workspace_test.id, 
                               display_name=testParameters['eventstream_name'], 
                               description=testParameters['eventstream_description'])
    yield es

@pytest.fixture(scope='session')
def test_eventhouse(fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]) -> Generator[Eventhouse, None, None]:
    eh = fc.eventhouse.create(workspace_id=workspace_test.id, 
                              display_name=testParameters['eventhouse_name'], 
                              description=testParameters['eventhouse_description'])
    yield eh
    fc.eventhouse.delete(workspace_id=workspace_test.id, eventhouse_id=eh.id)

@pytest.fixture(scope='session')
def test_kqlDatabase(fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str], test_eventhouse:Eventhouse) -> Generator[KQLDatabase, None, None]:
    kqldb = fc.kqldatabase.create_readwrite_database(workspace_id=workspace_test.id, 
                                                     parentEventhouseItem_id=test_eventhouse.id,
                                                     display_name=testParameters['kqlDatabase_name'], 
                                                     description=testParameters['kqlDatabase_description'])
    yield kqldb

@pytest.fixture(scope='session')
def test_kqlDashboard(fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str], test_kqlDashboard: KQLDashboard) -> Generator[KQLDashboard, None, None]:
    kqlDashboard = fc.kqldashboard.create(workspace_id=workspace_test.id,
                                         display_name=testParameters['kqlDashboard_displayName'],
                                         definition=testParameters['kqlDashboard_definition'],
                                         description=testParameters['kqlDashboard_description'])
    yield kqlDashboard