"""Module providing Core Warehouse functions."""

from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.warehouse import Warehouse



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

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses",
            auth=self._auth,
            json=body
        )
        return Warehouse(**resp.body)

    def delete(self, workspace_id:uuid.UUID, warehouse_id:uuid.UUID) -> FabricResponse:
        """
        Delete Warehouse

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/delete-warehouse?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses/{warehouse_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:uuid.UUID, warehouse_id:uuid.UUID) -> Warehouse:
        """
        Get Warehouses

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/get-warehouse?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses/{warehouse_id}",
            auth=self._auth
        )
        warehouse = Warehouse(**resp.body)
        return warehouse

    def ls(self, workspace_id:uuid.UUID) -> Iterator[Warehouse]:
        """
        List Warehouses

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/list-warehouses?tabs=HTTP)
        """
        resp = _http._get_http_paged(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses",
            auth=self._auth,
            items_extract=lambda x:x["value"]
        )
        for page in resp:
            for item in page.items:
                yield Warehouse(**item)

    def update(self, workspace_id:uuid.UUID, warehouse_id:uuid.UUID, display_name:str=None, description:str=None) -> Warehouse:
        """
        Updates the properties of the specified warehouse

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/update-warehouse?tabs=HTTP)

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
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses/{warehouse_id}",
            auth=self._auth,
            json=body
        )
        warehouse = Warehouse(**resp.body)
        return warehouse
