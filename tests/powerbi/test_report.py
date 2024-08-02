from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.report import Report

class TestReportLifeCycle:

    def test_report_ls(self, fc: FabricClient, workspace_test: Workspace, test_report:Report):
        rpts = fc.report.ls(workspace_id=workspace_test.id)
        for r in list(rpts):
            if r.id == test_report.id:
                assert True
                return

    def test_report_get(self, fc: FabricClient, workspace_test: Workspace, test_report:Report):
        sm = fc.report.get(workspace_id=workspace_test.id, report_id=test_report.id)
        assert sm is not None

    def test_report_update_definition(self, fc: FabricClient, workspace_test: Workspace, test_report:Report, rpt_definition:dict):
        res = fc.report.update_definition(workspace_id=workspace_test.id, report_id=test_report.id, definition=rpt_definition)
        assert res.is_successful is True

    def test_report_get_definition(self, fc: FabricClient, workspace_test: Workspace, test_report:Report):
        definition = fc.report.get_definition(workspace_id=workspace_test.id, report_id=test_report.id)
        assert definition['parts'] is not None

    def test_report_clone(self, fc: FabricClient, workspace_test: Workspace, test_report:Report):
        cloned = fc.report.clone(source_workspace_id=workspace_test.id, 
                                 report_id=test_report.id, 
                                 clone_name=f'{test_report.name}_cloned',
                                 target_workspace_id=workspace_test.id)
        assert cloned is not None
        if cloned is not None:
            fc.report.delete(workspace_id=workspace_test.id, report_id=cloned.id)    

    def test_report_delete(self, fc: FabricClient, workspace_test: Workspace, test_report:Report):
        resp = fc.report.delete(workspace_id=workspace_test.id, report_id=test_report.id)
        assert resp.is_successful is True
        
        
    
