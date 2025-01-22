from pydantic import AliasChoices, Field

from needlr.models.item import ItemType, Item


class Lakehouse(Item):
    name: str = Field(validation_alias=AliasChoices('displayName'))
    type: ItemType = ItemType.Lakehouse
