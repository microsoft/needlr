
import uuid

from pydantic import AliasChoices, BaseModel, Field

from needlr.models.item import ItemType, Item


class Warehouse(Item):
    name: str = Field(validation_alias=AliasChoices('displayName'))
    type: ItemType = ItemType.Warehouse
