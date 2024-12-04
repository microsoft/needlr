"""Module providing an Admin Workspace."""

from enum import Enum
import uuid
from pydantic import BaseModel
from needlr.models.git import AzureDevOpsDetails, GitHubDetails
from needlr.models.workspace import WorkspaceRole, WorkspaceType, PrincipalType
from typing import List, Union

class WorkspaceState(str, Enum):
    """
    The workspace state. Additional workspace states may be added over time.

    [WorkspaceState](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/get-workspace?tabs=HTTP#workspacestate)
    """
    Active = 'Active'
    Deleted = 'Deleted'

class Workspace(BaseModel):
    """
        This is the Admin Workspace definition for the Admin Workspace Client.
        This model is slightly different from the Core Workspace model.

    capacityId: string - The capacity ID of the workspace.
    id: string - The workspace ID. ( Item )
    name: string - The workspace name.
    state: WorkspaceState - The workspace state.
    type: WorkspaceType - The workspace type.

    """
    id: uuid.UUID = None
    capacityId: uuid.UUID = None
    name: str = None
    state: WorkspaceState = None
    type: WorkspaceType = None

class GitConnectionDetails(BaseModel):
    """
       Represents the details of a Git connection for a workspace.

       [GitConnectionDetails](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-git-connections?tabs=HTTP#gitconnectiondetails)

        gitProviderDetails	- The provider details.
        workspaceId	- The workspace ID.

    """
    #gitProviderDetails: GitProviderDetails = None
    gitProviderDetails: Union[AzureDevOpsDetails, GitHubDetails] = None
    workspaceId: uuid.UUID = None

class GroupType(str, Enum):
    """
   The type of the group. Additional group types may be added over time.

    [GroupType](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspace-access-details?tabs=HTTP#grouptype)

    DistributionList -String - Principal is a distribution list.
    SecurityGroup - GroupDetails - 	Principal is a security group.
    Unknown - string - Principal group type is unknown.

    """
    DistributionList = 'DistributionList'
    SecurityGroup = 'SecurityGroup'
    Unknown = 'Unknown'

class GroupDetails(BaseModel):
    """
    Group specific details. Applicable when the principal type is Group.
    [GroupDetails](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspace-access-details?tabs=HTTP#groupdetails)

    groupType -GroupType - The type of the group. Additional group types may be added over time.

    """
    groupType: GroupType = None

class ServicePrincipalDetails(BaseModel):
    """
    Service principal specific details. Applicable when the principal type is ServicePrincipal.

    [ServicePrincipalDetails](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspace-access-details?tabs=HTTP#serviceprincipaldetails)

    aadAppId -string - The service principal's Microsoft Entra AppId.
    
    """
    aadAppId: str = None

class UserDetails(BaseModel):
    """
   User principal specific details. Applicable when the principal type is User.

    [UserDetails](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspace-access-details?tabs=HTTP#userdetails)

    userPrincipalName -string - The user principal name.
    

    """
    userPrincipalName: str = None

class Principal(BaseModel):
    """
    Represents an identity or a Microsoft Entra group.

    [Principal](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspace-access-details?tabs=HTTP#principal)

    displayName -String - The principal's display name.
    groupDetails - GroupDetails - Workspace permissions for the user.
    id - string - The principal's ID.
    servicePrincipalDetails - ServicePrincipalDetails - Service principal specific details. Applicable when the principal type is ServicePrincipal.
    servicePrincipalProfileDetails - ServicePrincipalProfileDetails - Service principal profile details. Applicable when the principal type is ServicePrincipalProfile.
    type - PrincipalType - The type of the principal. Additional principal types may be added over time.
    userDetails - UserDetails - User principal specific details. Applicable when the principal type is User.

    """
    displayName: str = None
    groupDetails: GroupDetails = None
    id: str = None
    servicePrincipalDetails: ServicePrincipalDetails = None
    # TODO: Figure out this circular reference to Principal
    #servicePrincipalProfileDetails: ServicePrincipalProfileDetails = None
    type: PrincipalType = None
    userDetails: UserDetails = None

class ServicePrincipalProfileDetails(BaseModel):
    """
    Service principal profile details. Applicable when the principal type is ServicePrincipalProfile.

    [ServicePrincipalProfileDetails](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspace-access-details?tabs=HTTP#serviceprincipalprofiledetails)

    parentPrincipal - Principal - The service principal profile's parent principal.

    """
    parentPrincipal: Principal = None

class WorkspaceAccessDetail(BaseModel):
    """
    Workspace permission details.
    [WorkspaceAccessDetail](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspace-access-details?tabs=HTTP#workspaceaccessdetail)

    type -WorkspaceType - Workspace type.
    workspaceRole - WorkspaceRole - The workspace role.

    """
    type: WorkspaceType = None
    workspaceRole: WorkspaceRole = None

class WorkspaceAccessDetails(BaseModel):
    """
    User access details for the workspace.
    [WorkspaceAccessDetails](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspace-access-details?tabs=HTTP#workspaceaccessdetails)

    principal -Principal - Information regarding the user who has access to the entity.
    workspaceAccessDetails - WorkspaceAccessDetail - Workspace permissions for the user.

    """
    principal: Principal = None
    workspaceAccessDetails: WorkspaceAccessDetail = None

class WorkspaceAccessDetailsResponse(BaseModel):
    """
       A list of users with access to a given entity.

       [WorkspaceAccessDetailsResponse](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspace-access-details?tabs=HTTP#workspaceaccessdetailsresponse)

       accessDetails -WorkspaceAccessDetails[] - A list of users with access to an entity.

    """
    accessDetails: List[WorkspaceAccessDetails] = None