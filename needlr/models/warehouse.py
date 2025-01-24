from enum import Enum

from pydantic import AliasChoices, Field

from needlr.models.item import ItemType, Item

class WarehouseCollation(str, Enum):
    """
    [Reference](https://learn.microsoft.com/en-us/fabric/data-warehouse/collation)
    """
    CASE_SENSITIVE = 'Latin1_General_100_BIN2_UTF8'
    CASE_INSENSITIVE = 'Latin1_General_100_CI_AS_KS_WS_SC_UTF8'

class Warehouse(Item):
    name: str = Field(validation_alias=AliasChoices('displayName'))
    type: ItemType = ItemType.Warehouse
