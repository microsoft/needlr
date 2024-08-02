"""Module providing Core Datamart functions."""

from collections.abc import Iterator
import uuid

from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.datamart import Datamart



class _DatamartClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/datamart/items)

    ### Coverage

    * List Datamarts > ls()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a Datamart.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL for the Datamart.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def ls(self, workspace_id:uuid.UUID) -> Iterator[Datamart]:
            """
            List Datamarts

            Retrieves a list of Datamarts associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.

            Yields:
                Iterator[Datamart]: An iterator of Datamart objects.

            Reference:
                [List Datamart](GET https://learn.microsoft.com/en-us/rest/api/fabric/datamart/items/list-datamarts?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/datamarts",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield Datamart(**item)
