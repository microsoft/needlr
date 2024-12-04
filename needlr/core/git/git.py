"""Module providing Core Git functions."""

from needlr import _http
from requests import Response
from needlr.auth.auth import _FabricAuthentication
from needlr._http import FabricResponse
from needlr.models.git import (
    GitStatusResponse,
    CommitToGitRequest,
    ItemIdentifier,
    CommitMode,
    GitProviderDetails,
    AzureDevOpsDetails,
    GitHubDetails,
    GitConnection,
    InitializeGitConnectionRequest,
    WorkspaceConflictResolution,
    UpdateOptions,
    UpdateFromGitRequest,
    InitializeGitConnectionResponse
)

from pydantic import BaseModel
import uuid

class _GitClient:
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git)

    Methods:

    get_status: Return the Git Status of items in the workspace that can be committed to Git

    """

    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a GitClient object.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the role.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def commit_to_git(
        self, workspace_id: uuid.UUID, mode: str, comment: str, items: list[ItemIdentifier]
    ) -> FabricResponse:
        """
        Commits the changes made in the workspace to the connected remote branch.
        This API supports long running operations (LRO).
        You can choose to commit all changes or only specific changed items. To sync the workspace for the first time, use this API after the Connect and Initialize Connection APIs.

        Parameters:
        - workspace_id (uuid.UUID): The ID of the workspace for the commit to act on.
        - mode:  Modes for the Commit operation.  Refer to (https://learn.microsoft.com/en-us/rest/api/fabric/core/git/commit-to-git?tabs=HTTP#commitmode)
        - comment:  The comment that will be assigned for the commmit.
        - items: A list of items to be added if the mode is Selective:  Refer to (https://learn.microsoft.com/en-us/rest/api/fabric/core/git/commit-to-git?tabs=HTTP#itemidentifier)

        Reference:
        - [Git - Commit to Git](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/commit-to-git?tabs=HTTP)
        """

        # get the workspacehead string which is required for the body to the commit
        gitStatus = self.get_status(workspace_id)
        wsh = gitStatus.workspaceHead

        # TODO Throw an exception for a bad mode?
        # if mode != CommitMode.All or CommitMode.Selective:

        #if gitStatus.changes.count > 0:

        body = {"mode": mode, "workspaceHead": wsh, "comment": comment}

        if mode == CommitMode.Selective:  # only add the items if the mode if selective

            if items:
                body["items"] = items

        # 10.21.24 Confered with Bret.  If an attempt to commit fails due to a lack of items needing to be committed,
        # a 400 error is raised with the message -- "errorCode":"NoChangesToCommit","message":"There are no changes to commit."

        resp = _http._post_http_long_running(
            url=f"{self._base_url}workspaces/{workspace_id}/git/commitToGit",
            auth=self._auth,
            item=CommitToGitRequest(**body),
        )
        return resp
            


    def connect(self, workspace_id: uuid.UUID, gpd: GitProviderDetails) -> FabricResponse:
        """
        Connect a specific workspace to a git repository and branch.

        This operation does not sync between the workspace and the connected branch.
        To complete the sync, use the Initialize Connection operation and follow with either the Commit To Git or the Update From Git operation.

            Parameters:
            - workspace_id (uuid.UUID): The ID of the workspace where the item will be created.
            - GitProviderDetails( GitProviderDetails): The details of the Git provider to connect to.

            Reference:
            - [Git - Connect](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/connect?tabs=HTTP)
        """
        # print(GitProviderDetails.model_dump_json(indent=2))

        class AzureRepo(BaseModel):
            gitProviderDetails: AzureDevOpsDetails

        class GitHubRepo(BaseModel):
            gitProviderDetails: GitHubDetails

        if isinstance(gpd, AzureDevOpsDetails):

            det = AzureRepo(gitProviderDetails=gpd)

        elif isinstance(gpd, GitHubDetails):

            det = GitHubRepo(gitProviderDetails=gpd)

        else:
            raise TypeError("Unsupported type")

        resp = _http._post_http(
            url = self._base_url+f"workspaces/{workspace_id}/git/connect",
            auth=self._auth,
            json=det.model_dump(),
            responseNotJson=True
        )
        return resp

    def disconnect(self, workspace_id: uuid.UUID) -> FabricResponse:
        """
        Disconnect a specific workspace from the Git repository and branch it is connected to.

            Parameters:
            - workspace_id (uuid.UUID): The ID of the workspace to disconnect the repository from.

            Reference:
            - [Git - Connect](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/disconnect?tabs=HTTP)
        """
        resp = _http._post_http(
            url = self._base_url+f"workspaces/{workspace_id}/git/disconnect",
            auth=self._auth,
            responseNotJson=True
        )
        return resp

    def get_connection(self, workspace_id: uuid.UUID) -> GitConnection:
        """
        Returns git connection details for the specified workspace.

        Parameters:
        - workspace_id (uuid.UUID): The ID of the workspace for the connection details.

        Returns:
            GitConnection -  A GitConnection object representing the connection details.

        Reference:
        - [Git - Get Connection](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-connection?tabs=HTTP)
        """
        # print( "Getting status for url: "+ self._base_url+f"workspaces/{workspace_id}/git/status")

        # resp = _http._get_http(
        #     url=self._base_url + f"workspaces/{workspace_id}/git/connection",
        #     auth=self._auth,
        #     items_extract=lambda x: x["changes"],
        # )
        resp = _http._get_http(
            url=self._base_url + f"workspaces/{workspace_id}/git/connection",
            auth=self._auth
        )

        localBody = resp.body

        if localBody['gitConnectionState'] == 'NotConnected':

            del localBody['gitProviderDetails']
            del localBody['gitSyncDetails']

        else:    
                
            if localBody['gitProviderDetails']['gitProviderType'] == 'AzureDevOps':
                gpd = AzureDevOpsDetails(**localBody['gitProviderDetails'])  

            elif localBody['gitProviderDetails']['gitProviderType'] == 'GitHub':
                gpd = GitHubDetails(**localBody['gitProviderDetails'])

            del localBody['gitProviderDetails']

            #update the body with the new gitProviderDetails
            localBody['gitProviderDetails'] = gpd.model_dump()

        gitConnection = GitConnection(**localBody)
        return gitConnection

    def get_status(self, workspace_id: uuid.UUID) -> GitStatusResponse:
        """
        Returns the Git status of items in the workspace, that can be committed to Git.
        This API supports long running operations (LRO).
        The status indicates changes to the item(s) since the last workspace and remote branch sync. If both locations were modified, the API flags a conflict.

        Parameters:
        - workspace_id (uuid.UUID): The ID of the workspace where the item will be created.

        Returns:
            [Iterator]GitStatusResponse An iterator that yields Workspace objects representing each workspace.

        Reference:
        - [Git - Get Status](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-status?tabs=HTTP)
        """
        # print( "Getting status for url: "+ self._base_url+f"workspaces/{workspace_id}/git/status")

        resp = _http._get_http(
            url=self._base_url + f"workspaces/{workspace_id}/git/status",
            auth=self._auth,
            items_extract=lambda x: x["changes"],
        )

        # convert the None to 'None' for the response due to the impedence mismatch between the API and the model
        # None va 'None'
        # TODO: Find a better way of handling this and document this needed.
        for k,v in resp.body.items():
            if v is None:
                resp.body[k] = 'None'
            if k == 'changes':
                for change in v:
                    for k2,v2 in change.items():
                        if v2 is None:
                            change[k2] = 'None'

        #print( json.dumps(resp.body ))        

        return GitStatusResponse(**resp.body)

    def initialize_connection(self, workspace_id: str, initializationStrategy: str ) -> InitializeGitConnectionResponse:
        """
       Initialize a connection for a workspace that is connected to Git.

        This API supports long running operations (LRO).

        This API should be called after a successful call to the Connect API. To complete a full sync of the workspace, use the Required Action operation to call the relevant sync operation, either Commit To Git or Update From Git.
        
        Parameters:
        - workspace_id (str): The ID of the workspace for the commit to act on.
        - initializationStrategy (InitializationStrategy): The strategy required for an initialization process when content exists on both the remote side and the workspace side.

        Returns:
            InitializeGitConnectionResponse:  Contains the initialize Git connection response data.

        Reference:
        - [Git - Commit to Git](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/initialize-connection?tabs=HTTP#initializegitconnectionresponse)
        """

        body = {"initializationStrategy": initializationStrategy}

        resp = _http._post_http_long_running(
            url=f"{self._base_url}workspaces/{workspace_id}/git/initializeConnection",
            auth=self._auth,
            item=InitializeGitConnectionRequest(**body),
        )

        # convert the None to 'None' for the response due to the impedence mismatch between the API and the model
        # None va 'None'
        # TODO: Find a better way of handling this and document this needed.
        for k,v in resp.body.items():
            if v is None:
                resp.body[k] = 'None'


        #print( json.dumps(resp.body ))

        return InitializeGitConnectionResponse(**resp.body)
    

    def update_from_git(
        self, workspace_id: uuid.UUID, conflictResolution: WorkspaceConflictResolution, options: UpdateOptions
    ) -> FabricResponse:
        """
        Updates the workspace with commits pushed to the connected branch.
        This API supports long running operations (LRO).
        The update only affects items in the workspace that were changed in those commits. 
        If called after the Connect and Initialize Connection APIs, it will perform a full update of the entire workspace.

        Parameters:
        - workspace_id (str): The ID of the workspace for the commit to act on.
        - conflictResolution(WorkspaceConflictResolution):  Conflict resolution to be used in the update from Git operation. If items are in conflict and a conflict resolution is not specified, the update operation will not start.
        - options(UpdateOptions):  Options to be used in the update from Git operation

        Reference:
        - [Git - Update From Git](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/update-from-git?tabs=HTTP)
        """

        # get the workspacehead string which is required for the body to the commit
        gitStatus = self.get_status(workspace_id)
        wsh = gitStatus.workspaceHead
        rch = gitStatus.remoteCommitHash

        body = {"conflictResolution": conflictResolution, "options": options, "remoteCommitHash": rch }

        if wsh != 'None': # only add the items if the mode if not Null
            body["workspaceHead"] = wsh
            

        resp = _http._post_http_long_running(
            url=f"{self._base_url}workspaces/{workspace_id}/git/updateFromGit",
            auth=self._auth,
            item=UpdateFromGitRequest(**body),
        )    
        return resp