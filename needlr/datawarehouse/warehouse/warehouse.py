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
        """
        Initializes a Warehouse object.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the warehouse.

        """        
        self._auth = auth
        self._base_url = base_url

    def create(self, display_name:str, workspace_id:uuid.UUID, description:str=None) -> Warehouse:
        """
        Create Warehouse

        This method creates a new warehouse in the data warehouse system.

        Args:
            display_name (str): The display name of the warehouse.
            workspace_id (uuid.UUID): The ID of the workspace where the warehouse will be created.
            description (str, optional): The description of the warehouse. Defaults to None.

        Returns:
            Warehouse: The created warehouse object.

        Reference:
        - [Create Warehouse](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/create-warehouse?tabs=HTTP)
        """
        body = {
            "displayName":display_name
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses",
            auth=self._auth,
            item=Warehouse(**body)
        )
        return Warehouse(**resp.body)

    def delete(self, workspace_id:uuid.UUID, warehouse_id:uuid.UUID) -> FabricResponse:
        """
        Delete Warehouse

        Deletes a warehouse with the specified `warehouse_id` in the given `workspace_id`.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            warehouse_id (uuid.UUID): The ID of the warehouse to be deleted.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
        - [Delete Warehouse](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/delete-warehouse?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses/{warehouse_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:uuid.UUID, warehouse_id:uuid.UUID) -> Warehouse:
        """
        Get Warehouses

        Retrieves a specific warehouse from the data warehouse.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            warehouse_id (uuid.UUID): The ID of the warehouse.

        Returns:
            Warehouse: The retrieved warehouse object.

        Reference:
        [Microsoft Documentation](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/get-warehouse?tabs=HTTP)
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

        This method retrieves a list of warehouses associated with the specified workspace ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.

        Returns:
            Iterator[Warehouse]: An iterator that yields Warehouse objects.

        Reference:
        - [List Warehouses](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/list-warehouses?tabs=HTTP)
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

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the warehouse.
            warehouse_id (uuid.UUID): The ID of the warehouse to update.
            display_name (str, optional): The new display name for the warehouse.
            description (str, optional): The new description for the warehouse.

        Returns:
            Warehouse: The updated warehouse object.

        Raises:
            ValueError: If both `display_name` and `description` are left blank.

        Reference:
            [Microsoft Docs](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/update-warehouse?tabs=HTTP)
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
