"""Module providing Notebook Models."""

from enum import Enum
from needlr.models.item import ItemType, Item
from pydantic import AliasChoices, BaseModel, Field


class PayloadType(str, Enum):
    """
    Modes for the commit operation. Additional modes may be added over time.

    [PayloadType](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP#payloadtype)

    InlineBase64 - Inline Base 64.

    """
    InlineBase64 = 'InlineBase64'


class NotebookDefinitionPart(BaseModel):
    """
    Notebook definition part object.
    
    [NotebookDefinitionPart](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP#notebookdefinitionpart)

    path	- The notebook part path.
    payload	- The notebook part payload.
    payloadType - The payload type.
    
    """

    path: str = None
    payload: str = None
    payloadType: PayloadType = None

class NotebookDefinition(BaseModel):
    """
    The format of the Notebook definition. Supported format: ipynb.
    
    [NotebookDefinition](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP#notebookdefinition)

    format	- The notebook public definition.
    parts	- A list of definition parts.
    
    """

    format: str = None
    parts: NotebookDefinitionPart = None

class CreateNotebookRequest(BaseModel):
    """
    Create notebook request payload.
    
    [CreateNotebookRequest](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP#createnotebookrequest)

    definition	- The notebook public definition.
    description	- The notebook description. Maximum length is 256 characters.
    displayName - The notebook display name. The display name must follow naming rules according to item type.
    """

    definition: NotebookDefinition = None
    description: str = None
    displayName: str = None

class Notebook(Item):
    """
    A notebook object.
    
    [Notebook](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP#notebook)

    """
    name: str = Field(validation_alias=AliasChoices('displayName'))
    type: ItemType = ItemType.Notebook

