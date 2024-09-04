"""Module providing Core Mirrored Warehouse functions."""

from collections.abc import Iterator
import uuid

from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.warehouse import Warehouse

class _MirroredWarehouseClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/mirroredwarehouse/items)

    ### Coverage

    * List Mirrored Warehouses > ls()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a MirroredWarehouse object.

        Args:
            auth (_FabricAuthentication): The authentication object used for accessing the warehouse.
            base_url (str): The base URL of the warehouse.

        """
        self._auth = auth
        self._base_url = base_url

    def ls(self, workspace_id:uuid.UUID) -> Iterator[Warehouse]:
        """
        List Mirrored Warehouses

        This method retrieves a list of mirrored warehouses for a given workspace ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.

        Returns:
            Iterator[Warehouse]: An iterator that yields Warehouse objects representing the mirrored warehouses.

        Reference:
        - [List Mirrored Warehouses](https://learn.microsoft.com/en-us/rest/api/fabric/mirroredwarehouse/items/list-mirrored-warehouses?tabs=HTTP)
        """
        resp = _http._get_http_paged(
            url = f"{self._base_url}workspaces/{workspace_id}/mirroredWarehouses",
            auth=self._auth,
            items_extract=lambda x:x["value"]
        )
        for page in resp:
            for item in page.items:
                yield Warehouse(**item)
