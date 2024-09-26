
import uuid

from pydantic import AliasChoices, BaseModel, Field

from needlr.models.item import ItemType, Item


class Eventstream(Item):
    name: str = Field(validation_alias=AliasChoices('displayName'))
    type: ItemType = ItemType.Eventstream