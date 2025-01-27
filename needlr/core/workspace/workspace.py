"""Module providing a Core Workspace functions."""

from collections.abc import Iterator
from needlr.core.item.item import _ItemClient
from needlr.core.git.git import _GitClient
from needlr.core.jobscheduler.jobscheduler import _JobSchedulerClient
from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.core.workspace.role import _WorkspaceRoleClient
from needlr.core.workspace.identity import _WorkspaceIdentityClient
from needlr.models.workspace import Workspace
from needlr.models.item import Item, ItemType


class _WorkspaceClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces)

    ### Coverage

    * Assign to Capacity > capacity_assign()
    * Unassign From Capacity > capacity_unassign()
    * Create Workspace > create()
    * Delete Workspace > delete()
    * Get Workspace > get()
    * List items in the workspace > item_ls()
    * List Workspaces > ls()
    * Update Workspace > update()
    
    * Delete Workspace Role Assignment > role_delete()

    * Get Workspace Role Assignments > role_ls()


    * Update Workspace Role Assignment > role_update()

    """
    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a new instance of the Workspace class.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL of the workspace.

        """
        self._auth = auth
        self._base_url = base_url
        self.item = _ItemClient()
        self.role = _WorkspaceRoleClient(auth, base_url)
        self.identity = _WorkspaceIdentityClient(auth, base_url)
        self.git = _GitClient( auth, base_url )
        self.jobScheduler = _JobSchedulerClient(auth=auth, base_url=self._base_url)

    def capacity_assign(self, workspace_id:str, capacity_id:str) -> FabricResponse:
            """
            Assign a Workspace to a Capacity

            This method assigns a workspace to a capacity. It requires the 'Capacity.ReadWrite.All' scope.

            Args:
                workspace_id (str): The ID of the workspace to be assigned.
                capacity_id (str): The ID of the capacity to assign the workspace to.

            Returns:
                FabricResponse: The response from the API call.

            Reference:
            - [Microsoft Documentation](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/assign-to-capacity?tabs=HTTP)
            """
            body = {
                "capacityId":capacity_id
            }
            resp = _http._post_http(
                url = self._base_url+f"workspaces/{workspace_id}/assignToCapacity",
                auth=self._auth,
                json=body,
                responseNotJson=True
            )
            return resp

    def capacity_unassign(self, workspace_id:str) -> FabricResponse:
            """
            Unassign a Workspace from a Capacity.

            This method allows you to unassign a workspace from a capacity. 
            It requires the 'Capacity.ReadWrite.All' scope to be included in your authentication.

            Args:
                workspace_id (str): The ID of the workspace to unassign.

            Returns:
                FabricResponse: The response from the API call.

            Reference:
            - [Microsoft Documentation](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/unassign-from-capacity?tabs=HTTP)
            """
            resp = _http._post_http(
                url = self._base_url+f"workspaces/{workspace_id}/unassignFromCapacity",
                auth=self._auth,
                responseNotJson=True
            )
            return resp

    def create(self, display_name:str, capacity_id:str, description:str=None) -> Workspace:
            """
            Create Workspace

            This method creates a new workspace with the given display name and capacity ID.

            Args:
                display_name (str): The display name of the workspace.
                capacity_id (str): The ID of the capacity associated with the workspace.
                description (str, optional): The description of the workspace. Defaults to None.

            Returns:
                Workspace: The newly created workspace.

            Reference:
            - [Create Workspace](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/create-workspace?tabs=HTTP)
            """
            body = {
                "displayName":display_name
            }
            if capacity_id:
                body["capacityId"] = capacity_id
            if description:
                body["description"] = description
            resp = _http._post_http(
                url = self._base_url+"workspaces",
                auth=self._auth,
                json=body
            )
            return Workspace(**resp.body)

    def delete(self, workspace_id:str) -> FabricResponse:
            """
            Delete Workspace

            This method deletes a workspace with the specified workspace ID.

            Args:
                workspace_id (str): The ID of the workspace to be deleted.

            Returns:
                FabricResponse: The response object containing the result of the delete operation.

            Reference:
            - [Delete Workspace](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/delete-workspace?tabs=HTTP)
            """
            resp = _http._delete_http(
                url = self._base_url+f"workspaces/{workspace_id}",
                auth=self._auth
            )
            return resp
    
    def get(self, workspace_id:str=None) -> Workspace:
            """
            Get a Workspace by ID.

            Retrieves a Workspace object based on the provided workspace ID.

            Args:
                workspace_id (str): The ID of the workspace to retrieve.

            Returns:
                Workspace: The retrieved Workspace object.

            Raises:
                None.

            Reference:
            - [Get Workspace](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/get-workspace?tabs=HTTP#workspaceinfo)
            """
            resp = _http._get_http(
                url = self._base_url+f"workspaces/{workspace_id}",
                auth=self._auth
            )
            workspace = Workspace(**resp.body)
            return workspace

    def item_ls(self, workspace_id:str, item_type:ItemType=None) -> Iterator[Item]:
            """
            Lists items in the workspace based on the given workspace ID and item type.

            Args:
                workspace_id (str): The ID of the workspace.
                item_type (ItemType, optional): The type of items to filter. Defaults to None.

            Returns:
                Iterator[Item]: An iterator of items that match the given workspace ID and item type.
            """
            return self.item.list_items_by_filter(base_url=self._base_url, item_type=item_type, workspace_id=workspace_id, auth=self._auth)

    def ls(self, **kwargs) -> Iterator[Workspace]:
            """
            List Workspaces

            This method lists the workspaces available in the system.

            Args:
                **kwargs: Additional keyword arguments that can be passed to customize the request.

            Returns:
                Iterator[Workspace]: An iterator that yields Workspace objects representing each workspace.

            Reference:
            - [List Workspaces](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/list-workspaces?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = self._base_url+"workspaces",
                auth=self._auth,
                items_extract=lambda x:x["value"],
                **kwargs
            )
            for page in resp:
                for item in page.items:
                    yield Workspace(**item)

    def update(self, workspace_id:str, display_name:str=None, description:str=None) -> Workspace:
            """
            Update a Principal's Role Assignment

            This method updates the display name and description of a workspace identified by the given workspace ID.

            Args:
                workspace_id (str): The ID of the workspace to update.
                display_name (str, optional): The new display name for the workspace. Defaults to None.
                description (str, optional): The new description for the workspace. Defaults to None.

            Returns:
                Workspace: The updated workspace object.

            Raises:
                ValueError: If both display_name and description are left blank.

            Reference:
            - [Microsoft Documentation](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/update-workspace-role-assignment?tabs=HTTP)
            """
            if ((display_name is None) and (description is None)):
                raise ValueError("display_name or description must be provided")

            body = dict()
            if display_name is not None:
                body["displayName"] = display_name
            if description is not None:
                body["description"] = description

            resp = _http._patch_http(
                url = self._base_url+f"workspaces/{workspace_id}",
                auth=self._auth,
                json=body
            )
            workspace = Workspace(**resp.body)
            return workspace
