import pytest

from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.git import GitStatusResponse, AzureDevOpsDetails, InitializeGitConnectionResponse

class TestGit:

    def test_workspace_git_connect(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str,str,str,str,str,str]):

        adod = AzureDevOpsDetails()

        adod.organizationName = testParameters['git_organization_name']
        adod.projectName = testParameters['git_project_name']
        adod.gitProviderType = testParameters['git_provider_type']
        adod.repositoryName = testParameters['git_repository_name']
        adod.branchName = testParameters['git_branch_name']
        adod.directoryName = testParameters['git_directory_name']

        resp = fc.workspace.git.connect(workspace_id=workspace_test.id, gpd=adod)
        assert resp.is_successful is True 

    @pytest.mark.order(after="test_workspace_git_connect")
    def test_workspace_git_initialize_connection(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str]):

        resp = fc.workspace.git.initialize_connection(workspace_id=workspace_test.id, initializationStrategy=testParameters['git_initialization_strategy'])
        assert type(resp) is InitializeGitConnectionResponse


    @pytest.mark.order(after="test_workspace_git_initialize_connection")
    def test_workspace_git_get_status(self, fc: FabricClient, workspace_test: Workspace):

        resp = fc.workspace.git.get_status(workspace_id=workspace_test.id)
        assert type(resp) is GitStatusResponse