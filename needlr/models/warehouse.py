
import uuid

from pydantic import AliasChoices, BaseModel, Field

from needlr.models.item import ItemType, Item


class Warehouse(Item):
    id: uuid.UUID = None
    name: str = Field(validation_alias=AliasChoices('displayName'))
    description: str = None
    type: ItemType = ItemType.Warehouse
    workspaceId: uuid.UUID = None
