"""Module providing Core Warehouse functions."""

from collections.abc import Iterator
from needlr.core.item.item import _ItemClient
from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.core.workspace.role import _WorkspaceRoleClient
from needlr.models.warehouse import Warehouse
from needlr.models.item import Item, ItemType

import uuid


class _WarehouseClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items)

    ### Coverage

    * Create Warehouse > create()
    * Delete Warehouse > delete()
    * Get Warehouse > get()
    * List Warehouses > ls()
    * Update Warehouse > update()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        self._auth = auth
        self._base_url = base_url
        #self.item = _ItemClient()

    def create(self, display_name:str, workspace_id:uuid.UUID, description:str=None) -> Warehouse:
        """
        Create Warehouse

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/create-warehouse?tabs=HTTP)
        """
        body = {
            "displayName":display_name
        }
        if description:
            body["description"] = description

        resp = _http._post_http(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses",
            auth=self._auth,
            json=body
        )
        return Warehouse(**resp.body)

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
    
    def get(self, workspace_id:str=None) -> Warehouse:
        """
        Get Workspaces

        Workspace name and region or workspace id (guid) make it unique.

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/get-workspace?tabs=HTTP#workspaceinfo)
        """
        resp = _http._get_http(
            url = self._base_url+f"workspaces/{workspace_id}",
            auth=self._auth
        )
        warehouse = Warehouse(**resp.body)
        return warehouse

    def ls(self, **kwargs) -> Iterator[Warehouse]:
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
                yield Warehouse(**item)

    def update(self, workspace_id:str, display_name:str=None, description:str=None) -> Warehouse:
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
        warehouse = Warehouse(**resp.body)
        return warehouse
