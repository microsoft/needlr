
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
