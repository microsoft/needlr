from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.eventstream import Eventstream

class TesteventstreamLifeCycle:

    def test_eventstream_ls(self, fc: FabricClient, workspace_test: Workspace, test_eventstream: Eventstream):
        ep = test_eventstream
        ehs = fc.eventstream.ls(workspace_id=workspace_test.id)
        assert len(list(ehs)) > 0

    def test_eventstream_get(self, fc: FabricClient, workspace_test: Workspace, test_eventstream: Eventstream):
        eh = fc.eventstream.get(workspace_id=workspace_test.id, eventstream_id=test_eventstream.id)
        assert eh is not None

    def test_eventstream_update_definition(self, fc: FabricClient, workspace_test: Workspace, test_eventstream: Eventstream,testParameters: dict[str, str]):
        res = fc.eventstream.update_definition(workspace_id=workspace_test.id, eventstream_id=test_eventstream.id, description='New'+testParameters['eventstream_description'], display_name='New'+testParameters['eventstream_name'])
        assert res.is_successful is True

    def test_eventstream_clone(self, fc: FabricClient, workspace_test: Workspace, test_eventstream: Eventstream):
        cloned = fc.eventstream.clone(source_workspace_id=workspace_test.id, eventstream_id=test_eventstream.id, target_workspace_id=workspace_test.id, clone_name="cloned_eventstream")
        assert cloned is not None

    def test_eventstream_delete(self, fc: FabricClient, workspace_test: Workspace, test_eventstream: Eventstream):
        ehs = fc.eventstream.ls(workspace_id=workspace_test.id)
        for e in ehs:
            resp = fc.eventstream.delete(workspace_id=workspace_test.id, eventstream_id=e.id)
            assert resp.is_successful is True
        
        
    
