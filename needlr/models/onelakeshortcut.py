"""Module providing OneLake Shortcuts Model."""

from pydantic import BaseModel
from enum import Enum
from typing import Optional

from pydantic import AliasChoices, Field

from needlr.models.item import Item

class OneLakeShortcutConflictPolicy(str, Enum):
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-shortcuts/create-shortcut?tabs=HTTP#shortcutconflictpolicy)
    """
    Abort = 'Abort'
    GenerateUniqueName = 'GenerateUniqueName'

class OneLakeShortcutType(str, Enum):
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-shortcuts/get-shortcut?tabs=HTTP#type)
    """
    AdlsGen2 = 'AdlsGen2'
    AmazonS3 = 'AmazonS3'
    Dataverse = 'Dataverse'
    ExternalDataShare = 'ExternalDataShare'
    GoogleCloudStorage = 'GoogleCloudStorage'
    OneLake = 'OneLake'
    S3Compatible = 'S3Compatible'

class OneLakeShortcutTarget_AdlsGen2(BaseModel):
    connectionId:str
    location:str
    subpath:str

class OneLakeShortcutTarget_AmazonS3(BaseModel):
    connectionId:str
    location:str
    subpath:str

class OneLakeShortcutTarget_Dataverse(BaseModel):
    connectionId:str
    deltaLakeFolder:str
    environmentDomain:str
    tableName:str

class OneLakeShortcutTarget_ExternalDataShareTarget(BaseModel):
    connectionId:str

class OneLakeShortcutTarget_GoogleCloudStorage(BaseModel):
    connectionId:str
    location:str
    subpath:str

class OneLakeShortcutTarget_OneLake(BaseModel):
    itemId:str
    path:str
    workspaceId:str

class OneLakeShortcutTarget_S3Compatible(BaseModel):
    bucket:str
    connectionId:str
    location:str
    subpath:str

class OneLakeShortcutTarget(BaseModel):
    type:OneLakeShortcutType = None
    adlsGen2: Optional[OneLakeShortcutTarget_AdlsGen2] = None
    amazonS3: Optional[OneLakeShortcutTarget_AmazonS3] = None
    dataverse: Optional[OneLakeShortcutTarget_Dataverse] = None
    externalDataShare: Optional[OneLakeShortcutTarget_ExternalDataShareTarget] = None
    googleCloudStorage: Optional[OneLakeShortcutTarget_GoogleCloudStorage] = None
    oneLake: Optional[OneLakeShortcutTarget_OneLake] = None
    s3Compatible: Optional[OneLakeShortcutTarget_S3Compatible] = None

class OneLakeShortcut(Item):
    name: str = Field(validation_alias=AliasChoices('displayName'))
    path: str
    target: OneLakeShortcutTarget
