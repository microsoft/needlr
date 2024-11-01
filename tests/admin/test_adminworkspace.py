import pytest

from needlr import FabricClient
from needlr.models.workspace import Workspace as ws
from needlr.models.adminworkspace import Workspace as adminWS
from needlr.models.adminworkspace import WorkspaceAccessDetails

class TestAdminWorkspace:

    def test_ls_no_args(self, fc: FabricClient, workspace_test: ws ):
        aws = fc.admin_workspaceclient.ls()
        assert len(list(aws)) > 0

    def test_ls_active_state(self, fc: FabricClient, workspace_test: ws ):
        aws = fc.admin_workspaceclient.ls(state='Active')
        assert len(list(aws)) > 0

    def test_ls_workspace_type(self, fc: FabricClient, workspace_test: ws ):
        aws = fc.admin_workspaceclient.ls(type='Workspace')
        assert len(list(aws)) > 0

    def test_ls_workspace_name(self, fc: FabricClient, workspace_test: ws ):
        aws = fc.admin_workspaceclient.ls(name=workspace_test.name)
        assert len(list(aws)) > 0

    def test_workspace_access_details_ls(self, fc: FabricClient, workspace_test: ws ):
        wad = fc.admin_workspaceclient.workspace_access_details_ls(workspace_id=workspace_test.id)
        assert len(list(wad)) > 0

    def test_git_connections_ls(self, fc: FabricClient, workspace_test: ws ):
        gcd = fc.admin_workspaceclient.git_connections_ls()
        assert len(list(gcd)) > 0         

    def test_get(self, fc: FabricClient, workspace_test: ws ):
        workspace = fc.admin_workspaceclient.get(workspace_id=workspace_test.id)
        assert type(workspace) is adminWS                 