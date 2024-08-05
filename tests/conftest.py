import random

import pytest
from needlr import auth, FabricClient
from needlr.models.workspace import Workspace

@pytest.fixture(scope='session')
def testParameters():
    new_number = str(random.randint(1000000000, 9999999999))
    ws_name = f'_needlr_{new_number}' 
    return {
        'workspace_name': ws_name,
        'capacity_id': '558B0068-C465-4249-895E-A3985CBE841C',
        'description': 'Workspace created by PyTest',
        'warehouse_name': 'my_test_warehouse',
        'warehouse_description': 'Warehouse created by PyTest',
        'principal_id': 'd93322d5-ba1e-4af6-8778-784c0944dd8b',
        'semanticmodel_name': 'SalesModel',
        'paginatedReport_name': 'SalesReportPaginatedReportNewName',
        'paginatedReport_description': 'SalesReportPaginatedReport Description',
        'report_name': 'SalesReport',
        'eventhouse_name': 'TestEventhouse',
        'eventhouse_description': 'Test Eventhouse Description',
        'eventstream_name': 'TestEventstream',
        'eventstream_description': 'Test Eventstream Description',
        'kqlDatabase_name': 'testkqlatabase',
        'kqlDatabase_description': 'Test KQLDatabase Description',
    }
@pytest.fixture(scope='session')
def fc() -> FabricClient:
    return FabricClient(auth=auth.FabricInteractiveAuth(scopes=['https://api.fabric.microsoft.com/.default']))

@pytest.fixture(scope='session')
def workspace_test(fc: FabricClient, testParameters) -> Workspace:
    ws = fc.workspace.create(display_name=testParameters['workspace_name'],
                             capacity_id=testParameters['capacity_id'], 
                             description=testParameters['description'])
    yield ws
    fc.workspace.delete(workspace_id=ws.id)