"""Module providing a Core Workspace and Role Models."""

from enum import Enum
import uuid
import json
from typing import Literal
from pydantic import BaseModel, Field, AliasChoices
from needlr.models.item import Item


class WorkspaceRole(str, Enum):
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/list-workspace-role-assignments?tabs=HTTP#workspacerole)
    """
    Admin = 'Admin'
    Contributor = 'Contributor'
    Member = 'Member'
    Viewer = "Viewer"

class PrincipalType(str, Enum):
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/list-workspace-role-assignments?tabs=HTTP#principaltype)
    """
    Group = 'Group'
    ServicePrincipal = 'ServicePrincipal'
    ServicePrincipalProfile = 'ServicePrincipalProfile'
    User = "User"

class _Principal(BaseModel):
    id: uuid.UUID
    type: PrincipalType = None

    def to_json(self):
        return json.loads(self.model_dump_json())

class GroupPrincipal(_Principal):
    type: Literal[PrincipalType.Group] = PrincipalType.Group

class ServicePrincipal(_Principal):
    type: Literal[PrincipalType.ServicePrincipal] = PrincipalType.ServicePrincipal

class UserPrincipal(_Principal):
    type: Literal[PrincipalType.User] = PrincipalType.User

class ServicePrincipalProfile(_Principal):
    type: Literal[PrincipalType.ServicePrincipalProfile] = PrincipalType.ServicePrincipalProfile

class WorkspaceType(str, Enum):
    """
    A workspace type. Additional workspace types may be added over time.

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

class Workspace(Item):
    """
        This is the Core Workspace definition for the Core Workspace Client.
        This model is slightly different from the Admin Workspace model.
    """

    name: str = Field(validation_alias=AliasChoices('displayName'))
    type: WorkspaceType = None
    capacityId: uuid.UUID = None
    capacityAssignmentProgress: CapacityAssignmentProgress = None
    workspaceIdentity: dict = None
