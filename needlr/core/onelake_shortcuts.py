"""Module providing OneLake Shortcuts Client."""

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.onelakeshortcut import OneLakeShortcut, OneLakeShortcutTarget, OneLakeShortcutConflictPolicy, OneLakeShortcutTarget_OneLake

import uuid

class _OneLakeShortcutsClient():
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-shortcuts)
    
    ### Coverage
    
    * Create Shortcut > create()
    * Delete Shortcut > delete()
    * Get Shortcut > get()
    * List Shortcuts > ls()
    
    """
    def __init__(self, auth:_FabricAuthentication, base_url:str):
        """
        Initializes a Shortcut client to support, get, update, delete operations on shortcuts.
        
        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the shortcut.
        
        """        
        self._auth = auth
        self._base_url = base_url

    def create(self, workspace_id:uuid.UUID, itemId:uuid.UUID, display_name:str,  path:str, target: OneLakeShortcutTarget, shortcutConflictPolicy:OneLakeShortcutConflictPolicy=OneLakeShortcutConflictPolicy.Abort.value) -> FabricResponse:
        """
        Creates a shortcut in the specified workspace.
        This API supports long running operations (LRO).
        
        Args:
            display_name (str): The display name of the shortcut.
            workspace_id (uuid.UUID): The ID of the workspace where the shortcut will be created.
            itemId (uuid.UUID): The ID of the item where the shortcut will be created.
            path (str): The path of the shortcut.
            target (OneLakeShortcutTarget): The target of the shortcut.
            shortcutConflictPolicy (OneLakeShortcutConflictPolicy): The conflict policy for the shortcut. Default is Abort.
        
        Returns:
            FabricResponse: The response object.
        
        Reference:
        - [Create Shortcut](https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-shortcuts/create-shortcut?tabs=HTTP)
        """
        body = {
            "name":display_name,
            "path":path,
            "target":target
        }
        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/items/{itemId}/shortcuts?shortcutConflictPolicy={shortcutConflictPolicy.value}",
            auth=self._auth,
            item=OneLakeShortcut(**body)
        )
        return resp

    def delete(self, workspace_id:uuid.UUID, itemId:uuid.UUID, shortcut_name:str, shortcut_path:str) -> FabricResponse:
        """
        Deletes a shortcut in the specified workspace.
        
        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the shortcut will be deleted.
            itemId (uuid.UUID): The ID of the item where the shortcut will be deleted. (e.g. lakehouse_id)
            shortcut_name (str): The name of the shortcut.
            shortcut_path (str): The path of the shortcut.
        
        Returns:
            FabricResponse: The response object.
        
        Reference:
        - [Delete Shortcut](https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-shortcuts/delete-shortcut?tabs=HTTP)
        """
        return _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/items/{itemId}/shortcuts/{shortcut_path}/{shortcut_name}",
            auth=self._auth
        )

    def get(self, workspace_id:uuid.UUID, itemId:uuid.UUID, shortcut_name:str, shortcut_path:str) -> OneLakeShortcut:
        """
        Gets a shortcut in the specified workspace.
        
        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the shortcut will be retrieved.
            itemId (uuid.UUID): The ID of the item where the shortcut will be retrieved. (e.g. lakehouse_id)
            shortcut_name (str): The name of the shortcut.
            shortcut_path (str): The path of the shortcut.
        
        Returns:
            Shortcut: The shortcut object.
        
        Reference:
        - [Get Shortcut](https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-shortcuts/get-shortcut?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/items/{itemId}/shortcuts/{shortcut_path}/{shortcut_name}",
            auth=self._auth
        )
        r = resp
        return OneLakeShortcut(resp)

    def ls(self, workspace_id:uuid.UUID, itemId:uuid.UUID, parentPath:str=None) -> list[OneLakeShortcut]:
        """
        Lists all shortcuts in the specified workspace.
        
        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the shortcuts will be listed.
            itemId (uuid.UUID): The ID of the item where the shortcuts will be listed. (e.g. lakehouse_id)
        
        Returns:
            list[Shortcut]: The list of shortcuts.
        
        Reference:
        - [List Shortcuts](https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-shortcuts/list-shortcuts?tabs=HTTP)
        """
        parent_path_url = f'?parentPath={parentPath}' if parentPath else ''
        resp = _http._get_http_paged(
            url = f"{self._base_url}workspaces/{workspace_id}/items/{itemId}/shortcuts{parent_path_url}",
            auth=self._auth,
            items_extract=lambda x:x['value']
        )
        for page in resp:
            for item in page.items:
                yield OneLakeShortcut(**item)