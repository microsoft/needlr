"""Module providing Core Capacity functions."""

from collections.abc import Iterator
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.git import GitStatusResponse, CommitToGitRequest, ItemIdentifier, CommitMode


class _GitClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git)

    Methods:

    get_status: Return the Git Status of items in the workspace that can be committed to Git

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
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

    def commit_to_git(self, workspace_id:str, mode:str, comment:str, items: list[ItemIdentifier]):
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
        #wsh = self.__getWorkspaceHead__(self, workspace_id)
        gitStatus = self.get_status( workspace_id )
        wsh = gitStatus.workspaceHead

        #TODO Maybe throw an exception is wsh has a null value

        #TODO Throw an exception for a bad mode?
        #if mode != CommitMode.All or CommitMode.Selective:

        body = {
                "mode": mode,
                "workspaceHead": wsh,
                "comment": comment
        }

        if mode == CommitMode.Selective:  # only add the items if the mode if selective
        
            if items:
                body["items"] = items

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/git/commitToGit",
            auth=self._auth,
            item=CommitToGitRequest(**body)
        ) 

    def get_status(self, workspace_id:str) -> GitStatusResponse:
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
        #print( "Getting status for url: "+ self._base_url+f"workspaces/{workspace_id}/git/status")

        resp = _http._get_http(
            url = self._base_url+f"workspaces/{workspace_id}/git/status",
            auth= self._auth,
            items_extract=lambda x:x["changes"]

        )

        return GitStatusResponse(**resp.body)
   
