import pytest
from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.report import Report
from needlr.models.datapipeline import Datapipeline

class TestDatapipelineLifeCycle:

    def test_datapipeline_ls(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Datapipeline):
        dp = fc.datapipeline.ls(workspace_id=workspace_test.id)
        for p in list(dp):
            if p.id == test_datapipeline.id:
                assert True
                return
            
    @pytest.mark.order(after="test_datapipeline_ls")
    def test_datapipeline_get(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Datapipeline):
        dp = fc.datapipeline.get(workspace_id=workspace_test.id, datapipeline_id=test_datapipeline.id)
        assert dp is not None

    @pytest.mark.order(after="test_datapipeline_get")
    def test_datapipeline_update_definition(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Datapipeline, datapipeline_definition:dict):
        res = fc.datapipeline.update_definition(workspace_id=workspace_test.id, datapipeline_id=test_datapipeline.id,definition=datapipeline_definition)
        assert res.is_successful is True

    @pytest.mark.order(after="test_datapipeline_update")
    def test_datapipeline_clone(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Datapipeline):
        cloned = fc.datapipeline.clone(source_workspace_id=workspace_test.id, 
                                 datapipeline_id=test_datapipeline.id, 
                                 clone_name=f'{test_datapipeline.name}_cloned',
                                 target_workspace_id=workspace_test.id)
        assert cloned is not None
        if cloned is not None:
            fc.datapipeline.delete(workspace_id=workspace_test.id, datapipeline_id=cloned.id)    

    @pytest.mark.order(after="test_datapipeline_clone")
    def test_run_on_demand_job(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Datapipeline):
        par =   { 
                "executionData": { 
                    "parameters": {
                    "param_waitsec": "10" 
                    } 
                } 
            }
        job_id = fc.datapipeline.run_on_demand_job(workspace_id=workspace_test.id, datapipeline_id=test_datapipeline.id, parameters=par)
        if job_id is not None:
            print(job_id)
            job_id_instance = fc.datapipeline.get_item_job_instance(workspace_id=workspace_test.id, datapipeline_id=test_datapipeline.id, job_instance_id=job_id)
            if job_id_instance is not None:
                print(job_id_instance)
                cancel_job_instance = fc.datapipeline.cancel_item_job_instance(workspace_id=workspace_test.id, datapipeline_id=test_datapipeline.id, job_instance_id=job_id)
                print(cancel_job_instance)
                assert cancel_job_instance.is_successful is True

    @pytest.mark.order(after="test_run_on_demand_job")
    @pytest.mark.order(after="test_datapipeline_clone")
    def test_datapipeline_delete(self, fc: FabricClient, workspace_test: Workspace, test_datapipeline:Datapipeline):
        resp = fc.datapipeline.delete(workspace_id=workspace_test.id, datapipeline_id=test_datapipeline.id)
        assert resp.is_successful is True
        
        
    
