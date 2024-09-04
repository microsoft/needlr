from needlr import FabricClient
from needlr.models.workspace import Workspace

class TestDashboardLifeCycle:

    def test_dashboard_ls(self, fc: FabricClient, workspace_test: Workspace):
        whs = fc.dashboardclient.ls(workspace_id=workspace_test.id)
        assert len(list(whs)) == 0 # No Dashboards created yet