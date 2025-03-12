from collections.abc import Iterator
from needlr import _http
import uuid
from ...auth.auth import _FabricAuthentication
from needlr.models.adminworkspace import Workspace, GitConnectionDetails, WorkspaceAccessDetails


class _AdminWorkspaceClient():
    """
    A client to support, get and list operations on Admin workspaces.    

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces)

    ### Coverage

    * Get Workspace > get()
    * List Git Connections > git_connections_ls()
    * List Workspace Access Details > workspace_access_details_ls()
    * List Workspaces > ls()
    

    ### Required Scopes
        Tenant.Read.All or Tenant.ReadWrite.All

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes an _AdminWorkspaceClient client to support, get and list operations on workspaces.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the notebook.

        """         
        self._auth = auth
        self._base_url = base_url
    
    def get(self, workspace_id:uuid.UUID) -> Workspace:
        """
        Get an Admin Workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.

        Returns:
            Workspace: The Admin Workspace based on the Workspace ID provided.

        [Workspace](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/get-workspace?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}admin/workspaces/{workspace_id}",
            auth=self._auth
        )
        return Workspace(**resp.body) 

    def git_connections_ls(self) -> Iterator[GitConnectionDetails]:
        """
        Returns a list of Git connections.

        This API supports pagination. A maximum of 1,000 records can be returned per request. With the continuous token provided in the response, you can get the next 1,000 records.

        kwargs: (URI Parameters)(https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-git-connections?tabs=HTTP#uri-parameters)
            continuationToken: string - Continuation token. Used to get the next items in the list.


        [List[GitConnections]](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-git-connections?tabs=HTTP#gitconnections)

        """
        resp = _http._get_http_paged(
            url = f"{self._base_url}admin/workspaces/discoverGitConnections",
            auth=self._auth,
            items_extract=lambda x:x["value"],
            #params = kwargs
        )
        for page in resp:
            for item in page.items:
                yield GitConnectionDetails(**item)  
    
    
    def workspace_access_details_ls(self, workspace_id:uuid.UUID) -> Iterator[WorkspaceAccessDetails]:
        """
        eturns a list of users (including groups and ServicePrincipals) that have access to the specified workspace.

        This API supports pagination. A maximum of 10,000 records can be returned per request. With the continuous token provided in the response, you can get the next 10,000 records.

        args: 
            workspace_id (uuid.UUID): The ID of the workspace.

        [List[WorkspaceAccessDetailsResponse]](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspace-access-details?tabs=HTTP#principaltype)

        """
        resp = _http._get_http_paged(
            url = f"{self._base_url}admin/workspaces/{workspace_id}/users",
            auth=self._auth,
            items_extract=lambda x:x["accessDetails"]
        )
        for page in resp:
            for item in page.items:
                yield WorkspaceAccessDetails(**item) 

    def ls(self, **kwargs) -> Iterator[Workspace]:
        """
        Returns a list of workspaces.

        This API supports pagination. A maximum of 10,000 records can be returned per request. With the continuous token provided in the response, you can get the next 10,000 records.

        kwargs: (URI Parameters)(https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspaces?tabs=HTTP#uri-parameters)
            capacityId: string - The capacity ID of the workspace. ex. capacityId=uuid.UUID('6bbf84a0-e6aa-4d32-a1f5-d20af7913348')
            name: string - The workspace name. ex. name='_needlr_8056469686'
            state: string - The workspace state. Supported states are active and deleted. ex. state='active'
            type: string - The workspace type. Supported types are personal, workspace, adminWorkspace. ex. type='personal'


        [List[Workspace]](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspaces?tabs=HTTP)

        """
        resp = _http._get_http_paged(
            url = f"{self._base_url}admin/workspaces",
            auth=self._auth,
            items_extract=lambda x:x["workspaces"],
            params = kwargs
        )
        for page in resp:
            for item in page.items:
                yield Workspace(**item)                
    
    # TODO Not sure why this is here -- verify with the team

    #def item_ls(self, type:str=None, capacity_id:str=None, state:str=None, workspace_id:str=None):
    #    return item._list_items_by_filter(base_url=self._base_url, type=type, capacity_id=capacity_id, state=state, workspace_id=workspace_id, auth=self._auth)
        