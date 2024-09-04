from dotenv import load_dotenv
import pytest
from needlr import auth, FabricClient
from needlr.models.workspace import Workspace
import os

# Loading an Environment Variable File with dotenv
load_dotenv()


@pytest.fixture(scope='session')
def testParameters():
    return {
        'workspace_name': 'my_test_workspace',
        'capacity_id': os.getenv('CAPACITY_ID'),  # unique
        'description': 'Workspace created by PyTest',
        'warehouse_name': 'my_test_warehouse',
        'warehouse_description': 'Warehouse created by PyTest',
        'principal_id': os.getenv('PRINCIPAL_ID'),  # unique
        'semanticmodel_name': 'SalesModel',
        'paginatedReport_name': 'SalesReportPaginatedReportNewName',
        'paginatedReport_description': 'SalesReportPaginatedReport Description',
        'report_name': 'SalesReport',
    }
@pytest.fixture(scope='session')
def fc() -> FabricClient:
    return FabricClient(auth=auth.FabricInteractiveAuth(scopes=['https://api.fabric.microsoft.com/.default']))

@pytest.fixture(scope='session')
def workspace_test(fc: FabricClient, testParameters) -> Workspace:
    ws = fc.workspace.create(display_name=testParameters['workspace_name'], capacity_id=testParameters['capacity_id'], description=testParameters['description'])
    yield ws
    fc.workspace.delete(workspace_id=ws.id)