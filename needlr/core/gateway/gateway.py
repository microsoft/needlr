"""Module providing Core Gateway functions."""

import pprint as pp

from collections.abc import Iterator
from needlr import _http
from needlr._http import FabricResponse
#from requests import Response
from needlr.auth.auth import _FabricAuthentication
#from needlr._http import FabricResponse, FabricException
from needlr.models.gateway import (
    ListGatewaysResponse,
    VirtualNetworkAzureResource,
    CreateVirtualNetworkGatewayRequest,
    VirtualNetworkGateway
)

#import json
#from pydantic import BaseModel
#import uuid

class _GatewayClient():
    """

    [_GatewayClient](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways)

    Methods:
    create_gateway - Creates a new gateway
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

    
    def create_gateway( self, capacityId: int, 
                        displayName: str, 
                        inactivityMinutesBeforeSleep: int, 
                        numberOfMemberGateways: int, 
                        type: str,
                        resourceGroupName: str,
                        subnetName: str,
                        subscriptionId: str,
                        virtualNetworkName: str) -> FabricResponse:
        """
        Creates a new Gateway.

        Parameters:
        - capacityId: The object ID of the Fabric license capacity.
        - displayName:  The display name of the virtual network gateway. Maximum length is 200 characters.
        - inactivityMinutesBeforeSleep:  The minutes of inactivity before the virtual network gateway goes into auto-sleep. Must be one of the following values: 30, 60, 90, 120, 150, 240, 360, 480, 720, 1440.
        - numberOfMemberGateways: The number of member gateways. A number between 1 and 7.
        - type: The type of gateway. Must be one of the following values: VirtualNetwork.
        - resourceGroupName: The name of the resource group.
        - subnetName: The name of the subnet.
        - subscriptionId: The subscription ID.
        - virtualNetworkName: The name of the virtual network.

        Reference:
        - [Gateways - Create Gatewayay](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/create-gateway?tabs=HTTP)
        """

        # TODO Check for nulls and empty strings

        # create the VirtualNetworkAzureResource object
        vnar = {"resourceGroupName":resourceGroupName, "subnetName":subnetName, "subscriptionId":subscriptionId,  "virtualNetworkName":virtualNetworkName}

        body = {"capacityId": capacityId, 
                "displayName": displayName, 
                "inactivityMinutesBeforeSleep": inactivityMinutesBeforeSleep,
                "numberOfMemberGateways": numberOfMemberGateways,
                "type": type,
                "virtualNetworkAzureResource": vnar}

        resp = _http._post_http(
            url=f"{self._base_url}gateways",
            auth=self._auth,
            item=CreateVirtualNetworkGatewayRequest(**body),
        )
        return resp
    
    
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
                url=self._base_url + "gateways",
                auth=self._auth
            )
            localBody = resp.body

            listGatewaysResponse = ListGatewaysResponse(**localBody)

            return listGatewaysResponse