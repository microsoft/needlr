import pytest
from needlr import auth, FabricClient
from needlr.models.semanticmodel import SemanticModel
from needlr.models.workspace import Workspace
import pickle

@pytest.fixture(scope='session')
def sm_definition():
    with open('tests/powerbi/semantic_model_definition.pkl', 'rb') as sample_semantic_model_definition:
        definition = pickle.load(sample_semantic_model_definition)
        yield definition

@pytest.fixture(scope='session')
def rpt_definition():
    with open('tests/powerbi/report_definition.pkl', 'rb') as sample_report_definition:
        definition = pickle.load(sample_report_definition)
        yield definition


@pytest.fixture(scope='session')
def test_semanticmodel(fc: FabricClient, workspace_test: Workspace, sm_definition:dict, testParameters: dict[str, str]):
    sm = fc.semanticmodel.create(workspace_id=workspace_test.id, definition=sm_definition, display_name=testParameters['semanticmodel_name'])
    yield sm

@pytest.fixture(scope='session')
def test_report(fc: FabricClient, workspace_test: Workspace, rpt_definition:dict, testParameters: dict[str, str]):
    rpt = fc.report.create(workspace_id=workspace_test.id, definition=rpt_definition, display_name=testParameters['report_name'])
    yield rpt
