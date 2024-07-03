"""Module providing a Core Workspace functions."""

from collections.abc import Iterator
from needlr.core import item
from needlr.core.item.item import _ItemClient
from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.core.workspace.role import _WorkspaceRoleClient
from needlr.models.workspace import Workspace
from needlr.models.item import Item, ItemType

class _WorkspaceClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces)

    ### Coverage

    * Add Workspace Role Assignment > role_assign()
    * Assign to Capacity > capacity_assign()
    * Create Workspace > create()
    * Delete Workspace > delete()
    * Delete Workspace Role Assignment > role_delete()
    * Get Workspace > get()
    * Get Workspace Role Assignments > role_ls()
    * List Workspaces > ls()
    * Unassign From Capacity > capacity_unassign()
    * Update Workspace > update()
    * Update Workspace Role Assignment > role_update()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        self._auth = auth
        self._base_url = base_url
        self.item = _ItemClient()
        self.role = _WorkspaceRoleClient(auth, base_url)
    # Alternative assign_to_capacity
    def capacity_assign(self, workspace_id:str, capacity_id:str) -> FabricResponse:
        """
        Assign a Workspace to a Capacity

        Make sure your scope includes Capacity.ReadWrite.All

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/assign-to-capacity?tabs=HTTP)
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

    # Alternative assign_to_capacity
    def capacity_unassign(self, workspace_id:str) -> FabricResponse:
        """
        Unassign a Workspace to a Capacity

        Make sure your scope includes Capacity.ReadWrite.All

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/unassign-from-capacity?tabs=HTTP)
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

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/create-workspace?tabs=HTTP)
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

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/delete-workspace?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = self._base_url+f"workspaces/{workspace_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:str=None) -> Workspace:
        """
        Get Workspaces

        Workspace name and region or workspace id (guid) make it unique.

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/get-workspace?tabs=HTTP#workspaceinfo)
        """
        resp = _http._get_http(
            url = self._base_url+f"workspaces/{workspace_id}",
            auth=self._auth
        )
        workspace = Workspace(**resp.body)
        return workspace

    def item_ls(self, workspace_id:str, item_type:ItemType=None) -> Iterator[Item]:
        return self.item.list_items_by_filter(base_url=self._base_url, item_type=item_type, workspace_id=workspace_id, auth=self._auth)

    def ls(self, **kwargs) -> Iterator[Workspace]:
        """
        List Workspaces

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/list-workspaces?tabs=HTTP)
        """
        # Implement retry / error handling / continuation token
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

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/update-workspace-role-assignment?tabs=HTTP)

        Raises ValueError if display_name and description are left blank
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
