"""Module providing Spark Job Definition Models."""

from enum import Enum
from pydantic import BaseModel
from needlr.models.item import ItemType, Item
from pydantic import AliasChoices, BaseModel, Field

class PayloadType(str, Enum):
    """
    Modes for the commit operation. Additional modes may be added over time.

    [PayloadType](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/create-spark-job-definition?tabs=HTTP#payloadtype)

    InlineBase64 - Inline Base 64.

    """
    InlineBase64 = 'InlineBase64'

class SparkJobDefinitionPublicDefinitionPart(BaseModel):
    """
    Spark Job Definition public definition part object.
    
    [SparkJobDefinitionPublicDefinitionPart](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/create-spark-job-definition?tabs=HTTP#sparkjobdefinitionpublicdefinitionpart)

    path	- The spark job definition part path.
    payload	- The spark job definition part payload.
    payloadType - The payload type.
    
    """

    path: str = None
    payload: str = None
    payloadType: PayloadType = None

class SparkJobDefinitionPublicDefinition(BaseModel):
    """
    The format of the spark job definition definition.
    
    [SparkJobDefinitionPublicDefinition](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/get-spark-job-definition-definition?tabs=HTTP#sparkjobdefinitionpublicdefinition)

    format	- The format of the item definition. Supported format: SparkJobDefinitionV1.
    parts	- A list of definition parts.    
    """

    format: str = None
    parts: list[SparkJobDefinitionPublicDefinitionPart] = None

class SparkJobDefinitionProperties(BaseModel):
    """
    A spark job definition properties object.
    
    [SparkJobDefinitionProperties](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/create-spark-job-definition?tabs=HTTP#sparkjobdefinitionproperties)

    oneLakeRootPath - OneLake path to the SparkJobDefinition root directory.
    """
    oneLakeRootPath: str = None

class SparkJobDefinition(Item):
    """
    A spark job definition object.
    
    [SparkJobDefinition](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/create-spark-job-definition?tabs=HTTP#sparkjobdefinition)

    properties - Spark Job Definition Properties 
    """
    name: str = Field(validation_alias=AliasChoices('displayName'))
    type: ItemType = ItemType.SparkJobDefinition
    properties: SparkJobDefinitionProperties = None