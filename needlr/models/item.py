"""Module providing Core Item Model."""

from enum import Enum
from typing import List, Optional
import uuid
from pydantic import BaseModel, Field


class ItemType(str, Enum):
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/list-items?tabs=HTTP#itemtype)
    """
    Dashboard = 'Dashboard'
    DataPipeline = 'DataPipeline'
    Datamart = 'Datamart'
    Environment = 'Environment'
    Eventhouse = 'Eventhouse'
    Eventstream = 'Eventstream'
    KQLDatabase = 'KQLDatabase'
    KQLQueryset = 'KQLQueryset'
    Lakehouse = 'Lakehouse'
    MLModel = 'MLModel'
    MirroredWarehouse = 'MirroredWarehouse'
    Notebook = 'Notebook'
    PaginatedReport = 'PaginatedReport'
    Report = 'Report'
    SQLEndpoint = 'SQLEndpoint'
    SemanticModel = 'SemanticModel'
    SparkJobDefinition = 'SparkJobDefinition'
    SynapseNotebook = 'SynapseNotebook'
    Warehouse = 'Warehouse'

class Item(BaseModel):
    id: uuid.UUID = None
    type: ItemType = None   # In case new types how up, this will be None
    displayName: str
    description: str = None
    # TODO: definition should be optional for ItemClient.update
    definition:dict = None
    workspaceId: uuid.UUID = None
    # TODO: properties should be optional for ItemClient.update
    properties: dict = None

class ItemDefinitionPart(BaseModel):
    path: str = None
    payload: str = None
    payloadType: str = None

class ItemDefinition(BaseModel):
    format_: Optional[str] = Field(default=None, alias='format')
    parts: List[ItemDefinitionPart] = []

class ItemDefinitionResponse(BaseModel):
    definition: ItemDefinition = None
