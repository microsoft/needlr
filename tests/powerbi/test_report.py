from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.report import Report

import pytest

class TestReportLifeCycle:

    def test_report_ls(self, fc: FabricClient, workspace_test: Workspace, test_report:Report):
        sm = fc.semanticmodel.ls(workspace_id=workspace_test.id)
        for s in list(sm):
            if s.id == test_report.id:
                assert True
                return

    def test_report_get(self, fc: FabricClient, workspace_test: Workspace, test_report:Report):
        sm = fc.semanticmodel.get(workspace_id=workspace_test.id, semanticmodel_id=test_report.id)
        assert sm is not None

    def test_report_update_definition(self, fc: FabricClient, workspace_test: Workspace, test_report:Report, sm_definition:dict):
        res = fc.semanticmodel.update_definition(workspace_id=workspace_test.id, semanticmodel_id=test_report.id, definition=sm_definition)
        assert res.is_successful is True

    def test_report_get_definition(self, fc: FabricClient, workspace_test: Workspace, test_report:Report):
        definition = fc.semanticmodel.get_definition(workspace_id=workspace_test.id, semanticmodel_id=test_report.id)
        assert definition['parts'] is not None

    def test_semantic_model_clone(self, fc: FabricClient, workspace_test: Workspace, test_report:Report):
        cloned = fc.semanticmodel.clone(workspace_id=workspace_test.id, semanticmodel_id=test_report.id, clone_name=f'{test_report.name}_cloned')
        assert cloned is not None
        if cloned is not None:
            fc.semanticmodel.delete(workspace_id=workspace_test.id, semanticmodel_id=cloned.id)    

    def test_report_delete(self, fc: FabricClient, workspace_test: Workspace, test_report:Report):
        resp = fc.semanticmodel.delete(workspace_id=workspace_test.id, semanticmodel_id=test_report.id)
        assert resp.is_successful is True
        
        
    
