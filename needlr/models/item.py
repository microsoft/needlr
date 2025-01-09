"""Module providing Core Item Model."""

from enum import Enum
import uuid
from pydantic import BaseModel


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
    definition:dict = None
    workspaceId: uuid.UUID = None
    properties: dict = None
    parentDomainId: str = None

