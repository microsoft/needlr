"""Module providing Core Capacity functions."""

from collections.abc import Iterator
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.git import (
    GitStatusResponse,
    CommitToGitRequest,
    ItemIdentifier,
    CommitMode,
    GitProviderDetails,
    AzureDevOpsDetails,
    GitHubDetails,
    GitConnection
)
from pydantic import BaseModel

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
        self, workspace_id: str, mode: str, comment: str, items: list[ItemIdentifier]
    ):
        """
        Commits the changes made in the workspace to the connected remote branch.
        This API supports long running operations (LRO).
        You can choose to commit all changes or only specific changed items. To sync the workspace for the first time, use this API after the Connect and Initialize Connection APIs.

        Parameters:
        - workspace_id (str): The ID of the workspace for the commit to act on.
        - mode:  Modes for the Commit operation.  Refer to (https://learn.microsoft.com/en-us/rest/api/fabric/core/git/commit-to-git?tabs=HTTP#commitmode)
        - comment:  The comment that will be assigned for the commmit.
        - items: A list of items to be added if the mode is Selective:  Refer to (https://learn.microsoft.com/en-us/rest/api/fabric/core/git/commit-to-git?tabs=HTTP#itemidentifier)

        Returns:
            [Iterator]GitStatusResponse An iterator that yields Workspace objects representing each workspace.

        Reference:
        - [Git - Commit to Git](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/commit-to-git?tabs=HTTP)
        """

        # get the workspacehead string which is required for the body to the commit
        # wsh = self.__getWorkspaceHead__(self, workspace_id)
        gitStatus = self.get_status(workspace_id)
        wsh = gitStatus.workspaceHead

        # TODO Maybe throw an exception is wsh has a null value

        # TODO Throw an exception for a bad mode?
        # if mode != CommitMode.All or CommitMode.Selective:

        body = {"mode": mode, "workspaceHead": wsh, "comment": comment}

        if mode == CommitMode.Selective:  # only add the items if the mode if selective

            if items:
                body["items"] = items

        resp = _http._post_http_long_running(
            url=f"{self._base_url}workspaces/{workspace_id}/git/commitToGit",
            auth=self._auth,
            item=CommitToGitRequest(**body),
        )

    def connect(self, workspace_id: str, gpd: GitProviderDetails):
        """
        Connect a specific workspace to a git repository and branch.

        This operation does not sync between the workspace and the connected branch.
        To complete the sync, use the Initialize Connection operation and follow with either the Commit To Git or the Update From Git operation.

            Parameters:
            - workspace_id (str): The ID of the workspace where the item will be created.
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

        _http._post_http(
            url = self._base_url+f"workspaces/{workspace_id}/git/connect",
            auth=self._auth,
            json=det.model_dump(),
            responseNotJson=True
        )

    def disconnect(self, workspace_id: str):
        """
        Disconnect a specific workspace from the Git repository and branch it is connected to.

            Parameters:
            - workspace_id (str): The ID of the workspace to disconnect the repository from.

            Reference:
            - [Git - Connect](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/disconnect?tabs=HTTP)
        """
        _http._post_http(
            url = self._base_url+f"workspaces/{workspace_id}/git/disconnect",
            auth=self._auth,
            responseNotJson=True
        )

    def get_connection(self, workspace_id: str) -> GitConnection:
        """
        Returns git connection details for the specified workspace.

        Parameters:
        - workspace_id (str): The ID of the workspace for the connection details.

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

    def get_status(self, workspace_id: str) -> GitStatusResponse:
        """
        Returns the Git status of items in the workspace, that can be committed to Git.
        This API supports long running operations (LRO).
        The status indicates changes to the item(s) since the last workspace and remote branch sync. If both locations were modified, the API flags a conflict.

        Parameters:
        - workspace_id (str): The ID of the workspace where the item will be created.

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

        return GitStatusResponse(**resp.body)

