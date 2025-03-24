from dotenv import load_dotenv
import random
import pytest
from typing import Generator
from needlr import auth, FabricClient
from needlr.models.workspace import Workspace
from needlr.models.domain import Domain
from needlr.models.mlmodel import MLModel
from needlr.models.mlexperiment import MLExperiment
from needlr.models.reflex import Reflex
from needlr.models.kqldashboard import KQLDashboard
import os

# Loading an Environment Variable File with dotenv
load_dotenv()


@pytest.fixture(scope='session')
def testParameters():
    new_number = str(random.randint(1000000000, 9999999999))
    ws_name = f'_needlr_{new_number}'
    ranDomainNum = random.randint(1, 1000)
    

    return {
        'workspace_id': os.getenv('WORKSPACE_ID'), # unique
        'workspace_name': ws_name,
        'capacity_id': os.getenv('CAPACITY_ID'),  # unique
        'description': 'Workspace created by PyTest',
        'warehouse_name': 'my_test_warehouse',
        'warehouse_description': 'Warehouse created by PyTest',
        'lakehouse_name': 'my_test_lakehouse',
        'lakehouse_description': 'Lakehouse created by PyTest',
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
        'domain_displayName': 'APICreatedDomainName'+str(ranDomainNum),
        'domain_description': 'This is an API Created Domain from PyTest.',
        'mlmodel_displayName': 'ML Model Display Name',
        'mlmodel_description': 'ML Model Description',
        'mlmodel_id': 'ML Model ID',
        'mlmodel_continuation_token': 'ML Model Continuation Token',
        'mlexperiment_displayName': 'ML Experiment Display Name',
        'mlexperiment_description': 'ML Experiment Description',
        'mlexperiment_id': 'The ML Experiment ID',
        'mlexperiment_continuation_token': 'Optional | A token for retrieving the next page of results',
        'reflex_displayName': 'Reflex Display Name',
        'reflex_definition': 'Reflex Public Definition',
        'reflex_description': 'Reflex Description',
        'reflex_format': 'Format of the Reflex public definition',
        'reflex_continuation_token': 'Optional | A token for retrieving the next page of results',
        'reflex_updateMetadata': 'Optional | Boolean | Update Item Metadata',
        'kqlDashboard_id': 'KQL Dashboard ID',
        'kqlDashboard_displayName': 'KQL Dashboard Display Name',
        'kqlDashboard_definition': 'KQL Dashboard Definition',
        'kqlDashboard_description': 'KQL Dashboard Description',
        'kqlDashboard_format': 'Format of the KQL Dashboard public definition',
        'kqlDashboard_continuation_token': 'Optional | A token for retrieving the next page of results',
        'kqlDashboard_updateMetadata': 'Optional | Boolean | Update Item Metadata'
    }
@pytest.fixture(scope='session')
def fc() -> FabricClient:
    if os.getenv('APP_ID'):
        authorization = auth.FabricServicePrincipal(
            client_id=os.getenv('APP_ID'),
            client_secret=os.getenv('APP_SECRET'),
            tenant_id=os.getenv('TENANT_ID')
        )
    else:
        authorization = auth.FabricInteractiveAuth()
    return FabricClient(auth=authorization)

@pytest.fixture(scope='session')
def workspace_test(fc: FabricClient, testParameters) -> Generator[Workspace, None, None]:
    ws = fc.workspace.create(display_name=testParameters['workspace_name'],
                             capacity_id=testParameters['capacity_id'], 
                             description=testParameters['description'])
    yield ws
    fc.workspace.delete(workspace_id=ws.id)
    
@pytest.fixture(scope='session')
def domain_test(fc: FabricClient, testParameters) -> Generator[Domain, None, None]:
    
    domain_info = fc.domain.create(display_name=testParameters['domain_displayName'],
                             parentDomainId="", 
                             description=testParameters['domain_description'])
    yield domain_info

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

@pytest.fixture(scope='session')
def reflex_test(fc: FabricClient, testParameters) -> Generator[Reflex, None, None]:
    r = fc.mlexperiment.create(workspace_id=testParameters['workspace_id'],
                                display_name=testParameters['reflex_displayName'],
                                definition=testParameters['reflex_definition'],
                                description=testParameters['reflex_description'])
    yield r

@pytest.fixture(scope='session')
def test_kqlDashboard(fc: FabricClient, testParameters) -> Generator[KQLDashboard, None, None]:
    kqlDashboard = fc.kqldashboard.create(workspace_id=testParameters['workspace_id'],
                                         display_name=testParameters['kqlDashboard_displayName'],
                                         definition=testParameters['kqlDashboard_definition'],
                                         description=testParameters['kqlDashboard_description'])
    yield kqlDashboard