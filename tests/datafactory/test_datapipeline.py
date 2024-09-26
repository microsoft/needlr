from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.report import Report

class TestDatapipelineLifeCycle:

    def test_datapipeline_ls(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Report):
        rpts = fc.datapipeline.ls(workspace_id=workspace_test.id)
        for r in list(rpts):
            if r.id == test_datapipeline.id:
                assert True
                return

    def test_datapipeline_get(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Report):
        sm = fc.datapipeline.get(workspace_id=workspace_test.id, report_id=test_datapipeline.id)
        assert sm is not None

    def test_datapipeline_update_definition(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Report, rpt_definition:dict):
        res = fc.datapipeline.update_definition(workspace_id=workspace_test.id, report_id=test_datapipeline.id, definition=rpt_definition)
        assert res.is_successful is True

    def test_datapipeline_get_definition(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Report):
        definition = fc.datapipeline.get_definition(workspace_id=workspace_test.id, report_id=test_datapipeline.id)
        assert definition['parts'] is not None

    def test_datapipeline_clone(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Report):
        cloned = fc.datapipeline.clone(source_workspace_id=workspace_test.id, 
                                 report_id=test_datapipeline.id, 
                                 clone_name=f'{test_datapipeline.name}_cloned',
                                 target_workspace_id=workspace_test.id)
        assert cloned is not None
        if cloned is not None:
            fc.datapipeline.delete(workspace_id=workspace_test.id, report_id=cloned.id)    

    def test_datapipeline_delete(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Report):
        resp = fc.datapipeline.delete(workspace_id=workspace_test.id, report_id=test_datapipeline.id)
        assert resp.is_successful is True
        
        
    
