
import uuid

from pydantic import AliasChoices, BaseModel, Field

from needlr.models.item import ItemType, Item


class KQLDatabase(Item):
    name: str = Field(validation_alias=AliasChoices('displayName'))
    type: ItemType = ItemType.KQLDatabase
    creationPayload: dict  = None
