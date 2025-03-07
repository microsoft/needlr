"""Module providing a Core Gateway Model."""

from enum import Enum
import uuid
from pydantic import BaseModel, AliasChoices, Field
from typing import List, Union


class GatewayType(str, Enum):
    """
    [GatewayType](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/list-gateways?tabs=HTTP#gatewaytype)

    OnPremises - string - The on-premises gateway.
    OnPremisesPersonal - string - OnPremisesPersonal
    VirtualNetwork - string - The virtual network gateway.

    """
    OnPremises = 'OnPremises'
    OnPremisesPersonal = 'OnPremisesPersonal'
    VirtualNetwork = 'VirtualNetwork'

class Gateway(BaseModel):
    """
    A list of gateways returned.
    
    """
    pass

class PublicKey(BaseModel):
    """
    [PublicKey](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/list-gateways?tabs=HTTP#publickey)

    exponent - string - The exponent of the public key.
    modulus - string - The modulus of the public key.
    
    """
    exponent: str = None
    modulus: str = None
    

class LoadBalancingSetting(str, Enum):
    """
    [LoadBalancingSetting](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/list-gateways?tabs=HTTP#loadbalancingsetting)

    DistributeEvenly - string - Requests will be distributed evenly among all enabled gateway cluster members.
    Failover - string - Requests will be sent to the first available gateway cluster member.

    """
    DistributeEvenly = 'DistributeEvenly'
    Failover = 'Failover'


class OnPremisesGateway(Gateway):
    """

    [OnPremisesGateway](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/list-gateways?tabs=HTTP#onpremisesgateway)

    allowCloudConnectionRefresh - boolean - Whether to allow cloud connections to refresh through this on-premises gateway. True - Allow, False - Do not allow.
    allowCustomConnectors - boolean - Whether to allow custom connectors to be used with this on-premises gateway. True - Allow, False - Do not allow.
    displayName - string - The display name of the on-premises gateway.
    id - string - The object ID of the gateway.
    loadBalancingSetting - LoadBalancingSetting - The load balancing setting of the on-premises gateway.
    numberOfMemberGateways - integer - The number of gateway members in the on-premises gateway.
    publicKey - PublicKey - The public key of the primary gateway member. Used to encrypt the credentials for creating and updating connections.
    type - string: OnPremises - The type of the gateway.
    version - string - The version of the installed primary gateway member.
    """

    allowCloudConnectionRefresh: bool = None
    allowCustomConnectors: bool = None
    displayName: str = Field(validation_alias=AliasChoices('displayName'))
    id: uuid.UUID = Field(validation_alias=AliasChoices('id'))
    loadBalancingSetting: LoadBalancingSetting = None
    numberOfMemberGateways: int = None
    publicKey: PublicKey = None
    type: str = None
    version: str = None

class OnPremisesGatewayPersonal(Gateway):
    """

    [OnPremisesGatewayPersonal](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/list-gateways?tabs=HTTP#onpremisesgatewaypersonal)

    id - string - The object ID of the gateway.
    publicKey - PublicKey - The public key of the primary gateway member. Used to encrypt the credentials for creating and updating connections.
    type - string: OnPremises, Personal - The type of the gateway.
    version - string - The version of the installed primary gateway member.
    """

    id: uuid.UUID = Field(validation_alias=AliasChoices('id'))
    publicKey: PublicKey = None
    type: str = None
    version: str = None

class VirtualNetworkAzureResource(BaseModel):
    """

    [VirtualNetworkAzureResource](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/list-gateways?tabs=HTTP#virtualnetworkazureresource)

    resourceGroupName - string - The name of the resource group
    subnetName - string - The name of the subnet
    subscriptionId - string: The subscription ID
    virtualNetworkName - string - The name of the virtual network
    """

    resourceGroupName: str = None
    subnetName: str = None
    subscriptionId: str = None
    virtualNetworkName: str = None

class VirtualNetworkGateway(Gateway):
    """

    [VirtualNetworkGateway](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/list-gateways?tabs=HTTP#virtualnetworkgateway)

    capacityId - string - The object ID of the Fabric license capacity.
    displayName - string - The display name of the on-premises gateway.
    id - string - The object ID of the gateway.
    inactivityMinutesBeforeSleep - integer - The load balancing setting of the on-premises gateway.
    numberOfMemberGateways - integer - The minutes of inactivity before the virtual network gateway goes into auto-sleep.
    type - string: VirtualNetwork - The type of the gateway.
    virtualNetworkAzureResource - VirtualNetworkAzureResource - The Azure virtual network resource.
    """

    capacityId: str = None
    displayName: str = Field(validation_alias=AliasChoices('displayName'))
    id: uuid.UUID = Field(validation_alias=AliasChoices('id'))
    inactivityMinutesBeforeSleep: int = None
    numberOfMemberGateways: int = None
    type: str = None
    virtualNetworkAzureResource: VirtualNetworkAzureResource = None


class ListGatewaysResponse(BaseModel):
    """

    [ListGatewaysResponse](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/list-gateways?tabs=HTTP#listgatewaysresponse)

    continuationToken - string - The token for the next result set batch. If there are no more records, it's removed from the response.
    continuationUri -string - The URI of the next result set batch. If there are no more records, it's removed from the response.
    gateway - A list of gateways returned.
        OnPremisesGateway[]
        OnPremisesGatewayPersonal[]
        VirtualNetworkGateway[]

    """

    continuationToken: str = None
    continuationUri: str = None
    value: List[Union[VirtualNetworkGateway, OnPremisesGatewayPersonal, OnPremisesGateway ]] = None

class CreateVirtualNetworkGatewayRequest(BaseModel):
    """

    [CreateVirtualNetworkGatewayRequest](https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/create-gateway?tabs=HTTP#createvirtualnetworkgatewayrequest)

    capacityId - string - The object ID of the Fabric license capacity.
    displayName -string - The display name of the virtual network gateway. Maximum length is 200 characters.
    inactivityMinutesBeforeSleep - integer - The minutes of inactivity before the virtual network gateway goes into auto-sleep. Must be one of the following values: 30, 60, 90, 120, 150, 240, 360, 480, 720, 1440.
    numberOfMemberGateways - integer - The number of member gateways. A number between 1 and 7.
    type - string - The type of the gateway. Must be VirtualNetwork. 
    virtualNetworkAzureResource - VirtualNetworkAzureResource - The Azure virtual network resource.

    """

    capacityId: str = None
    displayName: str = Field(validation_alias=AliasChoices('displayName'))
    inactivityMinutesBeforeSleep: int = None
    numberOfMemberGateways: int = None
    type: str = None
    virtualNetworkAzureResource: VirtualNetworkAzureResource = None    


