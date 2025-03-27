"""Module providing Core Item Model."""

from enum import Enum
import uuid
from pydantic import BaseModel, Field


class ItemType(str, Enum):
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/list-items?tabs=HTTP#itemtype)
    """
    ApacheAirflowProject = 'ApacheAirflowProject'
    Dashboard = 'Dashboard'
    DataPipeline = 'DataPipeline'
    Datamart = 'Datamart'
    Environment = 'Environment'
    Eventhouse = 'Eventhouse'
    Eventstream = 'Eventstream'
    GraphQLApi = 'GraphQLApi'
    KQLDashboard = 'KQLDashboard'
    KQLDatabase = 'KQLDatabase'
    KQLQueryset = 'KQLQueryset'
    Lakehouse = 'Lakehouse'
    MLExperiment = 'MLExperiment'
    MLModel = 'MLModel'
    MirroredDatabase = 'MirroredDatabase'
    MirroredWarehouse = 'MirroredWarehouse'
    MountedDataFactory = 'MountedDataFactory'
    Notebook = 'Notebook'
    OrgApp = 'OrgApp'
    PaginatedReport = 'PaginatedReport'
    Reflex = 'Reflex'
    Report = 'Report'
    SQLEndpoint = 'SQLEndpoint'
    SemanticModel = 'SemanticModel'
    SparkJobDefinition = 'SparkJobDefinition'
    Warehouse = 'Warehouse'

class Item(BaseModel):
    id: uuid.UUID = None
    type: ItemType | str = None  # In case new types show up, this will be None
    displayName: str
    description: str = None
    definition:dict = None
    workspaceId: uuid.UUID = None
    properties: dict = None
    parentDomainId: str = None