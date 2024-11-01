from dotenv import load_dotenv
import random
import pytest
from typing import Generator
from needlr import auth, FabricClient
from needlr.models.workspace import Workspace
import os

# Loading an Environment Variable File with dotenv
load_dotenv()


@pytest.fixture(scope='session')
def testParameters():
    new_number = str(random.randint(1000000000, 9999999999))
    ws_name = f'_needlr_{new_number}'
    return {
        'workspace_name': ws_name,
        'capacity_id': os.getenv('CAPACITY_ID'),  # unique
        'description': 'Workspace created by PyTest',
        'warehouse_name': 'my_test_warehouse',
        'warehouse_description': 'Warehouse created by PyTest',
        'principal_id': os.getenv('PRINCIPAL_ID'),  # unique
        'git_repository_name': os.getenv('GIT_REPOSITORY_NAME'),  # unique
        'git_organization_name': os.getenv('GIT_ORGANIZATION_NAME'),  # unique
        'git_project_name': os.getenv('GIT_PROJECT_NAME'),  # unique
        'git_provider_type': os.getenv('GIT_PROVIDER_TYPE'),  # unique
        'git_branch_name': os.getenv('GIT_BRANCH_NAME'),  # unique
        'git_directory_name': os.getenv('GIT_DIRECTORY_NAME'),  # unique
        'git_initialization_strategy': os.getenv('GIT_INITIALIZATION_STRATEGY'),  # unique
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
        'datapipeline_name': 'testdatapipeline',
        'datapipeline_description': 'Test Datapipeline Description',
        'notebook_name': 'Test API Created Notebook',
        'notebook_description': 'This is an API Create Notebook from the REST API Test Harness.',
    }
@pytest.fixture(scope='session')
def fc() -> FabricClient:
    return FabricClient(auth=auth.FabricInteractiveAuth(scopes=['https://api.fabric.microsoft.com/.default']))

@pytest.fixture(scope='session')
def workspace_test(fc: FabricClient, testParameters) -> Generator[Workspace, None, None]:
    ws = fc.workspace.create(display_name=testParameters['workspace_name'],
                             capacity_id=testParameters['capacity_id'], 
                             description=testParameters['description'])
    yield ws
    fc.workspace.delete(workspace_id=ws.id)