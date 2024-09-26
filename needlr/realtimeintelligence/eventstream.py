"""Module providing Core Eventstream functions."""

from typing import Optional
from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.eventstream import Eventstream
from needlr.models.item import Item



class _EvenstreamClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/eventstream/items/create-eventstream?tabs=HTTP)

    ### Coverage

    * Create Eventstream > create()
    * Delete Eventstream > delete()
    * Get Eventstream > get()
    * List Eventstream > ls()
    * Update Eventstream > update()
    * Clone Eventstream > clone()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a Eventstream object.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL for the Eventstream.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def create(self, workspace_id:uuid.UUID, display_name:str, description:str=None) -> Eventstream:
        """
        Create Eventstream

        This method creates a Eventstream in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Eventstream will be created.
            display_name (str): The display name of the Eventstream.
            description (str, optional): The description of the Eventstream. Defaults to None.

        Returns:
            SemanticModel: The created Eventstream.

        Reference:
        [Create Eventstream](POST https://learn.microsoft.com/en-us/rest/api/fabric/eventstream/items/create-eventstream?tabs=HTTP)
        """
        body = {
            "displayName":display_name
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/eventstreams",
            auth=self._auth,
            item=Eventstream(**body)
        )
        eventstream = Eventstream(**resp.body)
        return eventstream

    def delete(self, workspace_id:uuid.UUID, eventstream_id:uuid.UUID) -> FabricResponse:
        """
        Delete Eventstream

        Deletes a Eventstream from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            eventstream_id (uuid.UUID): The ID of the Eventstream.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete Eventstream](https://learn.microsoft.com/en-us/rest/api/fabric/eventstream/items/delete-eventstream?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/eventstreams/{eventstream_id}",
            auth=self._auth
        )
        return resp
  
    def get(self, workspace_id:uuid.UUID, eventstream_id:uuid.UUID) -> Eventstream:
        """
        Get Eventstream

        Retrieves a Eventstream from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the Eventstream.
            eventstream_id (uuid.UUID): The ID of the Eventstream to retrieve.

        Returns:
            Eventstream: The retrieved Eventstream.

        References:
            - [Get Eventstream](https://learn.microsoft.com/en-us/rest/api/fabric/Eventstream/items/get-Eventstream?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/eventstreams/{eventstream_id}",
            auth=self._auth
        )
        eventstream = Eventstream(**resp.body)
        return eventstream

    def ls(self, workspace_id:uuid.UUID) -> Iterator[Eventstream]:
            """
            List Eventstreams

            Retrieves a list of Eventstreams associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.

            Yields:
                Iterator[Eventstream]: An iterator of Eventstream objects.

            Reference:
                [List Eventstreams](https://learn.microsoft.com/en-us/rest/api/fabric/eventstream/items/list-eventstreams?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/eventstreams",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield Eventstream(**item)

    def update_definition(self, workspace_id:uuid.UUID, eventstream_id:uuid.UUID, description:str, display_name:str) -> FabricResponse:
        """
        Update Eventstream

        This method updates the definition of a Eventstream in Power BI.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Eventstream is located.
            eventstream_id (uuid.UUID): The ID of the Eventstream to update.
            display_name (str): The updated display_name of the Eventstream.
            description (str): The updated description of the Eventstream.

        Returns:
            Eventstream: The updated Eventstream object.

        Reference:
        - [Update Eventstream Definition]https://learn.microsoft.com/en-us/rest/api/fabric/Eventstream/items/update-Eventstream?tabs=HTTP)
        """
        body = dict()
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/eventstreams/{eventstream_id}",
            auth=self._auth,
            item=Item(**body)
        )
        return resp

    def clone(self, source_workspace_id: uuid.UUID, eventstream_id: uuid.UUID, clone_name: str,  target_workspace_id: Optional[uuid.UUID]) -> Eventstream:
        """
        Clones a Eventstream.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            Eventstream_id (uuid.UUID): The ID of the Eventstream to clone.
            clone_name (str): The name of the cloned Eventstream.
            workspace_id (uuid.UUID): Optional. The ID of the target workspace.

        Returns:
            Eventstream: The cloned Eventstream.
        """
        source_eventstream = self.get(workspace_id=source_workspace_id, eventstream_id=eventstream_id)
        if target_workspace_id is None:
            target_workspace_id = source_workspace_id
        return self.create(target_workspace_id, display_name=clone_name, description=source_eventstream.description)

