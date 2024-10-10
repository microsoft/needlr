"""Module providing Core Git Models."""

from enum import Enum
from pydantic import BaseModel
from typing import List, Union
from needlr.models.item import ItemType

class GitProviderDetails(BaseModel):
    """
    The Git provider details.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/connect?tabs=HTTP#gitproviderdetails)

    azureDevOpsDetails - Azure DevOps provider details.
    gitHubDetails - GitHub provider details.

    """
    #branchName: str = None
    #directoryName: str = None
    #repositoryName: str = None
   

    
class AzureDevOpsDetails(GitProviderDetails):
    """
    Azure DevOps provider details.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/connect?tabs=HTTP#azuredevopsdetails)

    branchName	- The branch name. Maximum length is 250 characters.
    directoryName - The directory name. Maximum length is 256 characters.
    gitProviderType - [ AzureDevOps ] A Git provider type. Additional provider types may be added over time.
    organizationName - The organization name. Maximum length is 100 characters.
    projectName - The project name. Maximum length is 100 characters.
    repositoryName - The repository name. Maximum length is 128 characters.
    """
    branchName: str = None
    directoryName: str = None
    repositoryName: str = None
   
    organizationName: str = None
    projectName: str = None
    gitProviderType: str = 'AzureDevOps'


    
class GitHubDetails(GitProviderDetails):
    """
    GitHub provider details.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/connect?tabs=HTTP#githubdetails)

    branchName	- The branch name. Maximum length is 250 characters.
    directoryName - The directory name. Maximum length is 256 characters.
    gitProviderType - [ GitHub ] A Git provider type. Additional provider types may be added over time.
    ownerName - The owner name. Maximum length is 100 characters.
    repositoryName - The repository name. Maximum length is 128 characters.

    """
    branchName: str = None
    directoryName: str = None
    repositoryName: str = None

    gitProviderType: str = 'GitHub'
    ownerName: str = None

class GitSyncDetails(BaseModel):
    """
    Contains the sync details.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-connection?tabs=HTTP#gitsyncdetails)

    head	- The full Secure Hash Algorithm 1 (SHA-1) of the synced commit ID.
    lastSyncTime - The date and time of last sync state


    """
    Head: str = None
    LastSyncTime: str = None

class GitConnectionState(str,Enum):
    """
    Git connection state. Additional connection state types may be added over time.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-connection?tabs=HTTP#gitconnectionstate)

    Connected	- Connected state.
    ConnectedAndInitialized - Connected and initialized state.
    NotConnected - Not connected state.

    """
    Connected = 'Connected'
    ConnectedAndInitialized = 'ConnectedAndInitialized'
    NotConnected = 'NotConnected'

class GitConnection(BaseModel):
    """
    Contains the Git connection details.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-connection?tabs=HTTP#gitconnection)

    gitConnectionState	- Git connection state. Additional connection state types may be added over time.
    gitProviderDetails	- The Git provider details.
    gitSyncDetails - Contains the sync details.

    """
    gitConnectionState: GitConnectionState = None
    gitProviderDetails: Union[AzureDevOpsDetails, GitHubDetails] = None
    gitSyncDetails: GitSyncDetails = None

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


class GitConnectRequest(BaseModel):
    """
    Contains the Git connect request data.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/connect?tabs=HTTP#gitconnectrequest)

    gitProviderDetails	- The Git provider details.

    """
    gitProviderDetails: GitProviderDetails = None


class GitProviderType(BaseModel):
    """
    A Git provider type. Additional provider types may be added over time.
    
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/git/connect?tabs=HTTP#gitprovidertype)

    AzureDevOps	- Azure DevOps provider.
    GitHub - GitHub provider.


    """
    AzureDevOps: str = None
    GitHub: str = None



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