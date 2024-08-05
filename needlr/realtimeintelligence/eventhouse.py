"""Module providing Core Eventhouse functions."""

from typing import Optional
from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.eventhouse import Eventhouse
from needlr.models.item import Item



class _EventhouseClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/eventhouse/items)

    ### Coverage

    * Create Eventhouse > create()
    * Delete Eventhouse > delete()
    * Get Eventhouse > get()
    * List Eventhouse > ls()
    * Update Eventhouse > update()
    * Clone Eventhouse > clone()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a Eventhouse object.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL for the Eventhouse.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def create(self, workspace_id:uuid.UUID, display_name:str, description:str=None) -> Eventhouse:
        """
        Create Eventhouse

        This method creates a Eventhouse in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Eventhouse will be created.
            display_name (str): The display name of the Eventhouse.
            description (str, optional): The description of the Eventhouse. Defaults to None.

        Returns:
            Eventhouse: The created Eventhouse.

        Reference:
        [Create Eventhouse](POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/eventhouses)
        """
        body = {
            "displayName":display_name
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/eventhouses",
            auth=self._auth,
            item=Eventhouse(**body)
        )
        return Eventhouse(**resp.body)

    def delete(self, workspace_id:uuid.UUID, eventhouse_id:uuid.UUID) -> FabricResponse:
        """
        Delete Eventhouse

        Deletes a Eventhouse from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            eventhouse_id (uuid.UUID): The ID of the Eventhouse.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete Eventhouse](https://learn.microsoft.com/en-us/rest/api/fabric/eventhouse/items/delete-eventhouse?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/eventhouses/{eventhouse_id}",
            auth=self._auth
        )
        return resp
  
    def get(self, workspace_id:uuid.UUID, eventhouse_id:uuid.UUID) -> Eventhouse:
        """
        Get Eventhouse

        Retrieves a Eventhouse from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the Eventhouse.
            eventhouse_id (uuid.UUID): The ID of the Eventhouse to retrieve.

        Returns:
            Eventhouse: The retrieved Eventhouse.

        References:
            - [Get Eventhouse](https://learn.microsoft.com/en-us/rest/api/fabric/eventhouse/items/get-eventhouse?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/eventhouses/{eventhouse_id}",
            auth=self._auth
        )
        eventhouse = Eventhouse(**resp.body)
        return eventhouse

    def ls(self, workspace_id:uuid.UUID) -> Iterator[Eventhouse]:
            """
            List Eventhouses

            Retrieves a list of Eventhouses associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.

            Yields:
                Iterator[Eventhouse]: An iterator of Eventhouse objects.

            Reference:
                [List Eventhouses](https://learn.microsoft.com/en-us/rest/api/fabric/eventhouse/items/list-eventhouses?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/eventhouses",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield Eventhouse(**item)

    def update_definition(self, workspace_id:uuid.UUID, eventhouse_id:uuid.UUID, description:str, display_name:str) -> Eventhouse:
        """
        Update Eventhouse

        This method updates the definition of a Eventhouse in Power BI.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Eventhouse is located.
            eventhouse_id (uuid.UUID): The ID of the Eventhouse to update.
            display_name (str): The updated display_name of the Eventhouse.
            description (str): The updated description of the Eventhouse.

        Returns:
            Eventhouse: The updated Eventhouse object.

        Reference:
        - [Update Eventhouse Definition]https://learn.microsoft.com/en-us/rest/api/fabric/eventhouse/items/update-eventhouse?tabs=HTTP)
        """
        body = dict()
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/eventhouses/{eventhouse_id}",
            auth=self._auth,
            item=Item(**body)
        )
        eventhouse = Eventhouse(**resp.body)
        return eventhouse

    def clone(self, source_workspace_id: uuid.UUID, eventhouse_id: uuid.UUID, clone_name: str,  target_workspace_id: Optional[uuid.UUID]) -> Eventhouse:
        """
        Clones a Eventhouse.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            eventhouse_id (uuid.UUID): The ID of the Eventhouse to clone.
            clone_name (str): The name of the cloned Eventhouse.

        Returns:
            Eventhouse: The cloned Eventhouse.
        """
        source_eventhouse = self.get(workspace_id=source_workspace_id, eventhouse_id=eventhouse_id)
        if target_workspace_id is None:
            target_workspace_id = source_workspace_id
        return self.create(target_workspace_id, display_name=clone_name, description=source_eventhouse.description)

