"""Module providing a Core Capacity Model."""

from enum import Enum
import uuid
from pydantic import BaseModel



class CapacityState(str, Enum):
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/capacities/list-capacities?tabs=HTTP#capacitystate)
    """
    Active = 'Active'
    Inactive = 'Inactive'

class Capacity(BaseModel):
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/capacities/list-capacities?tabs=HTTP#capacity)

    displayName - The capacity display name.
    id - The capacity ID.
    region - The region of the capacity.
    sku - The capacity SKU.
    state - The capacity state.

    """

    displayName: str
    id: uuid.UUID = None
    region: str = None
    sku: str = None
    state:CapacityState = None
    