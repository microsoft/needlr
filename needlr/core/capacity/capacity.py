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

    def list_capacities(self, base_url, auth:_FabricAuthentication, **kwargs) -> Iterator[Capacity]:
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
                url = base_url+"capacities",
                auth= auth,
                items_extract=lambda x:x["value"],
                **kwargs
            )
            for page in resp:
                for item in page.items:
                    yield Capacity(**item)