"""Module providing Core Git Models."""

from enum import Enum
from pydantic import BaseModel, Field, AliasChoices
from typing import List
from needlr.models.item import ItemType

class ChangeType(Enum):
    """
    A Change of an item.  Additional changed types may be added over time.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-status?tabs=HTTP#changetype)

    Added - A newly created item.
    Deleted - Item has been deleted.
    Modified - Item content has been modified.

    """
    Added = 'Added'
    Deleted = 'Deleted'
    Modified = 'Modified'
    null = None

class CommitMode(str, Enum):
    """
    Modes for the commit operation. Additional modes may be added over time.

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/commit-to-git?tabs=HTTP#commitmode)
    """
    All = 'All'
    Selective = 'Selective'

class ConflictType(str, Enum):
    """
    A change of an item in both workspace and remote. Additional changed types may be added over time.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-status?tabs=HTTP#conflicttype)

    Conflict - There are different changes to the item in the workspace and in remote Git.
    None - There are no changes to the item.
    SameChanges	- There are identical changes to the item in the workspace and in remote Git.

    """

    Conflict = 'Conflict'
    #null = Field(validation_alias=AliasChoices('None', None))
    none ='None'
    SameChanges = 'SameChanges'

class ItemIdentifier(BaseModel):
    """
    Contains the item identifier. At least one of the properties must be defined.

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-status?tabs=HTTP#itemidentifier)

    logicalId - The logical ID of the item. When the logical ID isn't available because the item is not yet added to the workspace, you can use the object ID.
    objectId - The object ID of the item. When the object ID isn't available because the item was deleted from the workspace, you can use the logical ID.

    """

    logicalId: str = None
    objectId: str = None

class ItemMetadata(BaseModel):
    """
    Contains the item metadata.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-status?tabs=HTTP#itemmetadata)

    displayName	- The display name of the item. Prefers the workspace item's display name if it exists, otherwise displayName uses the remote item's display name.
    itemIdentifier - The item identifier.
    itemType - The item type.

    """
    displayName: str = None
    itemIdentifier: ItemIdentifier = None
    itemType: ItemType = None

class ItemChange(BaseModel):
    """
    Contains the item's change information.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-status?tabs=HTTP#itemchange)

    conflictType - When there are changes on both the workspace side and the remote Git side.
    itemMetadata - The item metadata.
    remoteChange - Change on the remote Git side.
    workspaceChange	- Change on the workspace side.

    """
    conflictType: ConflictType = None
    itemMetadata: ItemMetadata = None
    remoteChange: ChangeType = None
    workspaceChange: ChangeType = None

class GitStatusResponse(BaseModel):
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-status?tabs=HTTP#gitstatusresponse)

    changes - A list of changes in remote Git that are not applied to the given workspace, and changes in the workspace that are not applied to remote Git.
    remoteCommitHash - Remote full SHA commit hash.
    workspaceHead - Full SHA hash that the workspace is synced to.

    """

    changes: List[ItemChange] = None
    remoteCommitHash: str = None
    workspaceHead: str = None

class CommitToGitRequest(BaseModel):
    """
    Contains the commit request.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/commit-to-git?tabs=HTTP#committogitrequest)

    comment - Caller-free comment for this commit. Maximum length is 300 characters. If no comment is provided by the caller, use the default Git provider comment.
    items - Specific items to commit. This is relevant only for Selective commit mode. The items can be retrieved from the Git Status API.
    mode - The mode for the commit operation. [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/commit-to-git?tabs=HTTP#committogitrequest)
    workspaceHead - Full SHA hash that the workspace is synced to. The hash can be retrieved from the Git Status API.

    """
    comment: str = None
    items: List[ItemIdentifier] = None
    mode: str = CommitMode.All
    workspaceHead: str = None