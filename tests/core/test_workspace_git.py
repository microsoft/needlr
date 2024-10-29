import pytest
from needlr.utils.util import FabricException

from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.notebook import Notebook
from needlr.models.git import (GitStatusResponse, 
                               AzureDevOpsDetails, 
                               InitializeGitConnectionResponse, 
                               GitConnection,
                               CommitMode,
                                UpdateOptions,
                                ConflictResolutionPolicy,
                                ConflictResolutionType,
                                WorkspaceConflictResolution
)

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
    def test_workspace_git_update_from_git(self, fc: FabricClient, workspace_test: Workspace):

        crt = ConflictResolutionType.Workspace
        crp = ConflictResolutionPolicy.PreferWorkspace

        conflictResolution = WorkspaceConflictResolution()
        conflictResolution.conflictResolutionType = crt
        conflictResolution.conflictResolutionPolicy = crp

        options = UpdateOptions()
        options.allowOverrideItems = True

        resp = fc.workspace.git.update_from_git( workspace_id=workspace_test.id, 
                                conflictResolution = conflictResolution, options = options)
        
        assert resp.is_successful is True 


    @pytest.mark.order(after="test_workspace_git_update_from_git")
    def test_workspace_git_get_status(self, fc: FabricClient, workspace_test: Workspace):

        resp = fc.workspace.git.get_status(workspace_id=workspace_test.id)
        assert type(resp) is GitStatusResponse

    @pytest.mark.order(after="test_workspace_git_get_status")
    def test_workspace_git_get_connection(self, fc: FabricClient, workspace_test: Workspace):

        resp = fc.workspace.git.get_connection(workspace_id=workspace_test.id)
        assert type(resp) is GitConnection

    # # Adding a new notebook so we can commit to the repo
    # @pytest.mark.order(after="test_workspace_git_get_connection")
    # def test_notebook_create(self, fc: FabricClient, workspace_test: Workspace):


    #     resp = fc.notebook.create(display_name='MyNewNotebook123', 
    #                             workspace_id=workspace_test.id, 
    #                             description='notebook_description')
        
    #     assert type(resp) is Notebook

    # update git with the new notebook with a CommitMode of All
    @pytest.mark.order(after="test_workspace_git_get_connection")
    def test_workspace_git_commit_to_git1(self, fc: FabricClient, workspace_test: Workspace, notebook_test: Notebook):
        c = 'This is an API full commit from the REST API after creating a new notebook.'
        resp = fc.workspace.git.commit_to_git(workspace_id=workspace_test.id, mode=CommitMode.All, comment=c, items=[])
        assert resp.is_successful is True        

    @pytest.mark.order(after="test_workspace_git_commit_to_git1")
    def test_notebook_delete(self, fc: FabricClient, workspace_test: Workspace, notebook_test: Notebook):
        resp = fc.notebook.delete(workspace_id=workspace_test.id, notebook_id=notebook_test.id)
        assert resp.is_successful is True 


    @pytest.mark.order(after="test_notebook_delete")
    def test_workspace_git_commit_to_git2(self, fc: FabricClient, workspace_test: Workspace, notebook_test: Notebook):
        c = 'This is an API full commit from the REST API after deleting the new notebook.'
        resp = fc.workspace.git.commit_to_git(workspace_id=workspace_test.id, mode=CommitMode.All, comment=c, items=[])
        assert resp.is_successful is True        


    # TODO - Add a test to update the notebook and commit to git with a CommitMode of Selective