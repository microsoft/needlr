
import uuid
from enum import Enum

from pydantic import BaseModel
from typing import List


class Domain(BaseModel):
    """
    Represents a domain or subdomain.

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/create-domain?tabs=HTTP#domain)

    contributorsScope - The domain contributors scope.
    description - The description of the domain
    displayName - The name of the domain.
    id - TThe domain object ID.
    parentDomainId - The domain parent object ID.

    """
    contributorsScope: str ='AllTenant'
    description: str = None
    displayName: str = None
    id: uuid.UUID = None
    parentDomainid: uuid.UUID = None


class ContributorsScopeType(str, Enum):
    """
    The contributor scope. Additional contributor scopes may be added over time.

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/update-domain?tabs=HTTP#contributorsscopetype)

    AdminsOnly - Tenant and domain admins only.
    AllTenant -  All the tenant's users.
    SpecificUsersAndGroups - Specific users and groups.

    """
    AdminsOnly =  'AdminsOnly'
    AllTenant = 'AllTenant'
    SpecificUsersAndGroups = 'SpecificUsersAndGroups'

class UpdateDomainRequest(BaseModel):
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/update-domain?tabs=HTTP#updatedomainrequest)

    contributorsScope - The domain contributors scope.
    description - The domain description. The description cannot contain more than 256 characters.
    displayName - The domain display name. The display name cannot contain more than 40 characters.

    """
    contributorsScope: ContributorsScopeType = None
    description: str
    displayName: str


class AssignDomainWorkspacesByCapacitiesRequest(BaseModel):
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/assign-domain-workspaces-by-capacities?tabs=HTTP#assigndomainworkspacesbycapacitiesrequest)

    capacitiesIds - The capacity IDs.

    """
    capacitiesIds: List[str] = None



class AssignDomainWorkspacesByIdsRequest(BaseModel):
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/assign-domain-workspaces-by-ids?tabs=HTTP#assigndomainworkspacesbyidsrequest)

    workspacesIds - The workspace IDs.

    """
    workspacesIds: List[str] = None

class UnassignDomainWorkspacesByIdsRequest(BaseModel):
    """
    The request payload for unassigning workspaces from a domain by workspace ID.

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/unassign-domain-workspaces-by-ids?tabs=HTTP#unassigndomainworkspacesbyidsrequest)

    workspacesIds - The workspace IDs.

    """
    workspacesIds: List[str] = None


class DomainWorkspace(BaseModel):
    """
    Represents a workspace in a domain.

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/list-domain-workspaces?tabs=HTTP#domainworkspace)

    displayName	- string The name of the workspace.
    id - string The workspace ID.

    """
    displayName: str = None
    id: uuid.UUID = None

class DomainWorkspaces(BaseModel):
    """
    A response wrapper for a list of all the workspaces assigned to a domain with a continuous token.

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/list-domain-workspaces?tabs=HTTP#domainworkspaces)

    continuationToken - The token for the next result set batch. If there are no more records, it's removed from the response.
    continuationUri - The URI of the next result set batch. If there are no more records, it's removed from the response.
    value - The list of all the workspaces assigned to the domain.


    """
    continuationToken: str = None
    continuationUri: str = None
    value: List[DomainWorkspace] = None  