"""Module providing Core Capacity functions."""

from collections.abc import Iterator
from needlr.core.item.item import _ItemClient
from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.core.workspace.role import _WorkspaceRoleClient
from needlr.core.workspace.identity import _WorkspaceIdentityClient
from needlr.models.workspace import Workspace
from needlr.models.capacity import Capacity, CapacityState

class _CapacityClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/capacities)

    ### Coverage

    * List capacities the principal can access (either administrator or a contributor). > ls()

    """

    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a Role object.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the role.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url    

    def list_capacities(self, **kwargs) -> Iterator[Capacity]:
            """
            List Capacities

            Returns a list of capacities the principal can access (either administrator or a contributor)

            Args:
                **kwargs: Additional keyword arguments that can be passed to customize the request.

            Returns:
                Iterator[Workspace]: An iterator that yields Workspace objects representing each workspace.

            Reference:
            - [List Workspaces](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/list-workspaces?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = self._base_url+"capacities",
                auth= self._auth,
                items_extract=lambda x:x["value"],
                **kwargs
            )
            for page in resp:
                for item in page.items:
                    yield Capacity(**item)