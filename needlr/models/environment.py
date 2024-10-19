"""Module providing Environment Models."""

from enum import Enum
from pydantic import BaseModel
from needlr.models.item import ItemType, Item
from pydantic import AliasChoices, BaseModel, Field

class EnvironmentPublishState(str, Enum):
    """
    Publish state. Additional state types may be added over time.

    [EnvironmentPublishState](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/create-environment?tabs=HTTP#environmentpublishstate)
    """
    Cancelled = "Cancelled"
    Cancelling = "Cancelling"
    Failed = "Failed"
    Running = "Running"
    Success = "Success"	
    Waiting = "Waiting"

class SparkLibraries(BaseModel):
    """
    Spark Libraries

    [SparkLibraries](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/create-environment?tabs=HTTP#sparklibraries)

    state - Publish state.
    """
    state:EnvironmentPublishState=None

class SparkSettings(BaseModel):
    """
    Spark Settings

    [SparkSettings](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/create-environment?tabs=HTTP#sparksettings)

    state - Publish state.
    """
    state:EnvironmentPublishState=None

class ComponentPublishInfo(BaseModel):
    """
    Publish info for each components in environment.

    [ComponentPublishInfo](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/create-environment?tabs=HTTP#componentpublishinfo)

    sparkLibraries - Spark Libraries publish information
    sparkSettings - Spark Settings publish information
    """
    sparkLibraries:SparkLibraries = None
    sparkSettings:SparkSettings = None

class PublishDetails(BaseModel):
    """
    Details of publish operation.

    [PublishDetails](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/create-environment?tabs=HTTP#publishdetails)

    componentPublishInfo - Environment component publish information.
    startTime - Start time of publish operation
    endTime - End time of publish operation.
    state - Publish state.
    targetVersion - Target verion to be published.
    """
    componentPublishInfo:ComponentPublishInfo = None
    startTime:str = None
    endTime:str = None
    state:EnvironmentPublishState = None
    targetVersion:str = None

class EnvironmentPublishInfo(BaseModel):
    """
    Environment publish information.

    [EnvironmentPublishInfo](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/create-environment?tabs=HTTP#environmentpublishinfo)

    publishDetails - Environment publish operation details.
    """
    publishDetails:PublishDetails = None

class Environment(Item):
    """
    An Environment item.

    [Environment](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/create-environment?tabs=HTTP#environment)

    properties - The environment properties
    """
    name: str = Field(validation_alias=AliasChoices('displayName'))
    type: ItemType = ItemType.Environment
    properties:EnvironmentPublishInfo = None