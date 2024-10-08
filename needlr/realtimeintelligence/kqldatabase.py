"""Module providing Core KQLDatabase functions."""

from typing import Optional
from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.kqldatabase import KQLDatabase
from needlr.models.item import Item



class _KQLDatabaseClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/kqldatabase/items)

    ### Coverage

    * Create Shortcut KQLDatabase > create_shortcut_database()
    * Create Shortcut KQLDatabase with Invitation Token > create_shortcut_with_invitation_token_database()
    * Create ReadWrite KQLDatabase > create_readwrite_database()
    * Delete KQLDatabase > delete()
    * Get KQLDatabase > get()
    * List KQLDatabase > ls()
    * Update KQLDatabase > update()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a KQLDatabase object.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL for the KQLDatabase.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def create_shortcut_database(self, workspace_id:uuid.UUID, display_name:str, parentEventhouseItem_id:uuid.UUID, sourceClusterUri:str, sourceDatabaseName:str,  description:str=None) -> KQLDatabase:
        """
        Create Shortcut KQLDatabase

        This method creates a Shortcut KQLDatabase in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the KQLDatabase will be created.
            display_name (str): The display name of the KQLDatabase.
            parentEventhouseItem_id (uuid.UUID): The parent eventhouse item ID.
            sourceClusterUri (str): The Shortcut source cluster URI.
            sourceDatabaseName (str): The Shortcut source database name.
            description (str, optional): The description of the KQLDatabase. Defaults to None.

        Returns:
            FabricResponse: The response from the create request.

        Reference:
        [Create KQLDatabase](POST https://learn.microsoft.com/en-us/rest/api/fabric/kqldatabase/items/create-kql-database?tabs=HTTP)
        """
        body = {
            "displayName":display_name,
            'creationPayload': {
                'databaseType': "Shortcut",
                'parentEventhouseItemId': parentEventhouseItem_id,
                'sourceClusterUri': sourceClusterUri,
                'sourceDatabaseName': sourceDatabaseName
            }
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlDatabases",
            auth=self._auth,
            item=KQLDatabase(**body)
        )
        kqldb = KQLDatabase(**resp.body)
        return kqldb

    def create_shortcut_with_invitation_token_database(self, workspace_id:uuid.UUID, display_name:str, invitationToken:str, parentEventhouseItem_id:uuid.UUID,  description:str=None) -> KQLDatabase:
        """
        Create Shortcut KQLDatabase

        This method creates a Shortcut KQLDatabase in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the KQLDatabase will be created.
            display_name (str): The display name of the KQLDatabase.
            invitationToken (str): The invitation token for the KQLDatabase.
            parentEventhouseItem_id (uuid.UUID): The parent eventhouse item ID.
            description (str, optional): The description of the KQLDatabase. Defaults to None.

        Returns:
            FabricResponse: The response from the create request.

        Reference:
        [Create KQLDatabase](POST https://learn.microsoft.com/en-us/rest/api/fabric/kqldatabase/items/create-kql-database?tabs=HTTP)
        """
        body = {
            "displayName":display_name,
            'creationPayload': {
                'databaseType': "Shortcut",
                'invitationToken': invitationToken,
                'parentEventhouseItemId': parentEventhouseItem_id,
            }
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlDatabases",
            auth=self._auth,
            item=KQLDatabase(**body)
        )
        kqldb = KQLDatabase(**resp.body)
        return kqldb

    def create_readwrite_database(self, workspace_id:uuid.UUID, display_name:str, parentEventhouseItem_id:uuid.UUID,  description:str=None) -> KQLDatabase:
        """
        Create RadWrite KQLDatabase

        This method creates a Shortcut KQLDatabase in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the KQLDatabase will be created.
            display_name (str): The display name of the KQLDatabase.
            parentEventhouseItem_id (uuid.UUID): The parent eventhouse item ID.
            description (str, optional): The description of the KQLDatabase. Defaults to None.

        Returns:
            FabricResponse: The response from the create request.

        Reference:
        [Create KQLDatabase](POST https://learn.microsoft.com/en-us/rest/api/fabric/kqldatabase/items/create-kql-database?tabs=HTTP)
        """
        body = {
            "displayName":display_name,
            'creationPayload': {
                'databaseType': "ReadWrite",
                'parentEventhouseItemId': str(parentEventhouseItem_id),
            }
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlDatabases",
            auth=self._auth,
            item=KQLDatabase(**body)
        )
        kqldb =  KQLDatabase(**resp.body)
        return kqldb

    def delete(self, workspace_id:uuid.UUID, kqlDatabase_id:uuid.UUID) -> FabricResponse:
        """
        Delete KQLDatabase

        Deletes a KQLDatabase from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            kqlDatabase_id (uuid.UUID): The ID of the KQLDatabase.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete KQLDatabase](https://learn.microsoft.com/en-us/rest/api/fabric/kqldatabase/items/delete-kql-database?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlDatabases/{kqlDatabase_id}",
            auth=self._auth
        )
        return resp
  
    def get(self, workspace_id:uuid.UUID, kqlDatabase_id:uuid.UUID) -> KQLDatabase:
        """
        Get KQLDatabase

        Retrieves a KQLDatabase from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the KQLDatabase.
            kqlDatabase_id (uuid.UUID): The ID of the KQLDatabase to retrieve.

        Returns:
            KQLDatabase: The retrieved KQLDatabase.

        References:
            - [Get KQLDatabase](https://learn.microsoft.com/en-us/rest/api/fabric/kqldatabase/items/get-kql-database?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlDatabases/{kqlDatabase_id}",
            auth=self._auth
        )
        kqlDatabase = KQLDatabase(**resp.body)
        return kqlDatabase

    def ls(self, workspace_id:uuid.UUID) -> Iterator[KQLDatabase]:
            """
            List KQLDatabases

            Retrieves a list of KQLDatabases associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.

            Yields:
                Iterator[KQLDatabase]: An iterator of KQLDatabase objects.

            Reference:
                [List KQLDatabases](https://learn.microsoft.com/en-us/rest/api/fabric/kqldatabase/items/list-kql-databases?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/kqlDatabases",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield KQLDatabase(**item)

    def update(self, workspace_id:uuid.UUID, kqlDatabase_id:uuid.UUID, description:str, display_name:str) -> KQLDatabase:
        """
        Update KQLDatabase

        This method updates the definition of a KQLDatabase in Power BI.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the KQLDatabase is located.
            kqlDatabase_id (uuid.UUID): The ID of the KQLDatabase to update.
            display_name (str): The updated display_name of the KQLDatabase.
            description (str): The updated description of the KQLDatabase.

        Returns:
            KQLDatabase: The updated KQLDatabase object.

        Reference:
        - [Update KQLDatabase Definition]https://learn.microsoft.com/en-us/rest/api/fabric/KQLDatabase/items/update-KQLDatabase?tabs=HTTP)
        """
        body = dict()
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlDatabases/{kqlDatabase_id}",
            auth=self._auth,
            item=Item(**body)
        )
        kqlDatabase = KQLDatabase(**resp.body)
        return kqlDatabase