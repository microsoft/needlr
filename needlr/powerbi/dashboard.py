"""Module providing Core Dashboard functions."""

from collections.abc import Iterator
import uuid

from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.dashboard import Dashboard



class _DashboardClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/dashboard/items)

    ### Coverage

    * List Dashvboards > ls()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a Dashboard.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL for the Dashboard.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def ls(self, workspace_id:uuid.UUID) -> Iterator[Dashboard]:
            """
            List Dashboards

            Retrieves a list of Dashboards associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.

            Yields:
                Iterator[Dashboard]: An iterator of Dashboard objects.

            Reference:
                [List Dashboards](GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dashboards)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/dashboards",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield Dashboard(**item)
