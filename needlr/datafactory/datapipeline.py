"""Module providing a Core Workspace functions."""

from typing import Optional
from collections.abc import Iterator
import uuid

from needlr.core.item.item import _ItemClient
from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.core.workspace.role import _WorkspaceRoleClient
from needlr.models.datapipeline import Datapipeline
from needlr.models.item import Item


class _DatapipelineClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/datapipeline/items)

    ### Coverage

    * Create Datapipeline > create()
    * Delete Datapipeline > delete()
    * Get Datapipeline > get()
    * List Datapipelines > ls()
    * Update Datapipeline > update()

    """
    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a new instance of the Datapipeline class.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL of the Datapipeline.

        """
        self._auth = auth
        self._base_url = base_url

    def create(self, workspace_id:uuid.UUID, display_name:str, description:str=None) -> Datapipeline:
        """
        Create Datapipeline

        This method creates a Datapipeline in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Datapipeline will be created.
            display_name (str): The display name of the Datapipeline.
            description (str, optional): The description of the Datapipeline. Defaults to None.

        Returns:
            Datapipeline: The created Datapipeline.

        Reference:
        [Create Datapipeline](https://learn.microsoft.com/en-us/rest/api/fabric/datapipeline/items/create-data-pipeline?tabs=HTTP)
        """
        body = {
            "displayName":display_name
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/dataPipelines",
            auth=self._auth,
            item=Datapipeline(**body)
        )
        datapipeline = Datapipeline(**resp.body)
        return datapipeline

    def delete(self, workspace_id:uuid.UUID, datapipeline_id:uuid.UUID) -> FabricResponse:
        """
        Delete Datapipeline

        Deletes a Datapipeline from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            datapipeline_id (uuid.UUID): The ID of the Datapipeline.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete Datapipeline](DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/Datapipelines/{DatapipelineId})
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/dataPipelines/{datapipeline_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:uuid.UUID, datapipeline_id:uuid.UUID) -> Datapipeline:
        """
        Get Datapipeline

        Retrieves a Datapipeline from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the Datapipeline.
            datapipeline_id (uuid.UUID): The ID of the Datapipeline to retrieve.

        Returns:
            Datapipeline: The retrieved Datapipeline.

        References:
            - [Get Datapipeline](https://learn.microsoft.com/en-us/rest/api/fabric/datapipeline/items/get-data-pipeline?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/dataPipelines/{datapipeline_id}",
            auth=self._auth
        )
        datapipeline = Datapipeline(**resp.body)
        return datapipeline

    def ls(self, workspace_id:uuid.UUID) -> Iterator[Datapipeline]:
            """
            List Datapipelines

            Retrieves a list of Datapipelines associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.

            Yields:
                Iterator[Datapipeline]: An iterator of Datapipeline objects.

            Reference:
                [List Datapipelines](https://learn.microsoft.com/en-us/rest/api/fabric/datapipeline/items/list-data-pipelines?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/dataPipelines",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield Datapipeline(**item)

    def update(self, workspace_id:uuid.UUID, datapipeline_id:uuid.UUID, display_name:str, description:str) -> Datapipeline:
        """
        Update  Datapipeline Definition

        This method updates the definition of a  Datapipeline in Power BI.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the  Datapipeline is located.
            Datapipeline_id (uuid.UUID): The ID of the  Datapipeline to update.
            definition (dict): The updated definition of the  Datapipeline.

        Returns:
            Datapipeline: The updated  Datapipeline object.

        Reference:
        - [Update  Datapipeline Definition](https://learn.microsoft.com/en-us/rest/api/fabric/datapipeline/items/update-data-pipeline?tabs=HTTP)
        """
        body = dict()
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        resp = _http._post_http(
            url = f"{self._base_url}workspaces/{workspace_id}/dataPipelines/{datapipeline_id}",
            auth=self._auth,
            item=Item(**body)
        )
        return resp


