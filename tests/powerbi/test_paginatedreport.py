from needlr import FabricClient
from needlr.models.workspace import Workspace
import uuid
import pytest

class TestPaginatedReportLifeCycle:

    def test_paginatedreport_ls(self, fc: FabricClient, workspace_test: Workspace):
        pr = fc.paginatedreportclient.ls(workspace_id=workspace_test.id)
        assert len(list(pr)) == 0 # No Paginated Reports created yet

    @pytest.mark.skip(reason="No Paginated Reports created yet. TGested outside Pytest")
    def test_paginatedreport_update_definition(self, fc: FabricClient, workspace_test: Workspace, paginatedReport_id:uuid.UUID,  testParameters: dict[str, str]):
        pr = fc.paginatedreportclient.update(workspace_id=workspace_test.id, paginatedReport_id=paginatedReport_id, display_name='New'+ testParameters['paginatedReport_name'], description=testParameters['paginatedReport_description'])
        assert pr.name == 'New'+ testParameters['paginatedReport_name']