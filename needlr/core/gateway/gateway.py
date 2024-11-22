"""Module providing Core Gateway functions."""

from collections.abc import Iterator
from needlr import _http
#from requests import Response
from needlr.auth.auth import _FabricAuthentication
#from needlr._http import FabricResponse, FabricException
from needlr.models.gateway import (
    ListGatewaysResponse
)

#import json
#from pydantic import BaseModel
#import uuid

class _GatewayClient():
    """

    [_GatewayClient](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways)

    Methods:
    list_gateways - Returns a list of all gateways the user has permission for, including on-premises, on-premises (personal mode), and virtual network gateways
    

    """

    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a GatewayClient object.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the role.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def list_gateways(self, **kwargs) -> ListGatewaysResponse:
            """
            List Gateways

            Returns a list of all gateways the user has permission for, including on-premises, on-premises (personal mode), and virtual network gateways

            Args:
                **kwargs: Additional keyword arguments that can be passed to customize the request.

            Returns:
                Iterator[ListGatewaysResponse]: An iterator that yields Workspace objects representing each workspace.

            Reference:
            - [List Workspaces](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/list-workspaces?tabs=HTTP)
                """
            resp = _http._get_http(
                url = self._base_url+"gateways",
                auth=self._auth
            )
            listGatewaysResponse = ListGatewaysResponse(**resp.body)
            return listGatewaysResponse       