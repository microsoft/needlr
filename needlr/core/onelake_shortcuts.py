"""Module providing OneLake Shortcuts Client."""

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.onelakeshortcut import OneLakeShortcut, OneLakeShortcutTarget, OneLakeShortcutConflictPolicy

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

    def create(self, workspace_id:uuid.UUID, itemId:uuid.UUID, display_name:str,  path:str, target: OneLakeShortcutTarget, shortcutConflictPolicy:OneLakeShortcutConflictPolicy=OneLakeShortcutConflictPolicy.Abort) -> OneLakeShortcut:
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
            Shortcut: The created shortcut object.
        
        Reference:
        - [Create Shortcut](https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-shortcuts/create-shortcut?tabs=HTTP)
        """
        body = {
            "name":display_name,
            "path":path,
            "target":target
        }
        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/items/{itemId}/shortcuts?shortcutConflictPolicy={shortcutConflictPolicy}",
            auth=self._auth,
            item=OneLakeShortcut(**body)
        )
        return OneLakeShortcut(resp)