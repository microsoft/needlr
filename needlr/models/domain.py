
import uuid

from pydantic import AliasChoices, BaseModel, Field


class Domain(BaseModel):
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/capacities/list-capacities?tabs=HTTP#capacity)

    contriubtorCcope - The domain contributors scope
    description - The description of the domain
    displayName - The capacity display name.
    id - The domain object ID.
    parentId - the domain parent object id

    """
    contributorScope:str ='AllTenant'
    description:str
    displayName: str
    id: uuid.UUID = None
    parentDomainid: uuid.UUID = None