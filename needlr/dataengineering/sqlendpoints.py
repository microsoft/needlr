"""Module providing SQL Endpoint functions."""

from collections.abc import Iterator
import uuid

from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.sqlendpoint import SQLEndpoint



class _SQLEndpointClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/sqlendpoint/items)

    ### Coverage

    * List SQL Endpoints > ls()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a SQL ENdpoint object.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the warehouse.

        """        
        self._auth = auth
        self._base_url = base_url

    def ls(self, workspace_id:uuid.UUID) -> Iterator[SQLEndpoint]:
        """
        List SQL Ednpoints

        This method retrieves a list of SQL endpoints from the specified workspace ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.

        Returns:
            Iterator[Warehouse]: An iterator that yields Warehouse objects.

        Reference:
        - [List SQL Endpoints](https://learn.microsoft.com/en-us/rest/api/fabric/sqlendpoint/items)
        """
        resp = _http._get_http_paged(
            url = f"{self._base_url}workspaces/{workspace_id}/sqlEndpoints",
            auth=self._auth,
            items_extract=lambda x:x["value"]
        )
        for page in resp:
            for item in page.items:
                yield SQLEndpoint(**item)