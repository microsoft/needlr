
import uuid

from pydantic import AliasChoices, BaseModel, Field

from needlr.models.item import ItemType


class Warehouse(BaseModel):
    id: uuid.UUID
    name: str = Field(validation_alias=AliasChoices('displayName'))
    description: str = None
    type: ItemType = None
    workspaceId: uuid.UUID = None
