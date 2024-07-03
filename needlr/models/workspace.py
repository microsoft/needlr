from enum import Enum

from pydantic import BaseModel, Field, AliasChoices
import uuid

class WorkspaceType(str, Enum):
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/get-workspace?tabs=HTTP#workspacetype)
    """
    AdminWorkspace = 'AdminWorkspace'
    Personal = 'Personal'
    Workspace = 'Workspace'

class CapacityAssignmentProgress(str, Enum):
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/get-workspace?tabs=HTTP#capacityassignmentprogress)
    """
    Completed = 'Completed'
    Failed = 'Failed'
    InProgress = 'InProgress'

class Workspace(BaseModel):
    id: uuid.UUID
    name: str = Field(validation_alias=AliasChoices('displayName'))
    description: str
    type: WorkspaceType = None
    capacityId: uuid.UUID = None
    capacityAssignmentProgress: CapacityAssignmentProgress = None
    workspaceIdentity: dict = None