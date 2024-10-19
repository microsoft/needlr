from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.environment import Environment

class _EnvironmentClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items)

    ### Coverage

    * Create Environment > create()
    * Delete Environment > delete()
    * Get Environment > get()
    * List Environments > ls()
    * Update Environment > update()

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

    def create(self, workspace_id:uuid.UUID, display_name:str, description:str=None) -> Environment:
        """
        Create Environment

        This method creates a Environment in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Environment will be created.
            display_name (str): The display name of the Environment.
            description (str, optional): The description of the Environment. Defaults to None.

        Returns:
            Environment: The created Environment.

        Reference:
        [Create Environment](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/create-environment?tabs=HTTP)
        """
        body = {
            "displayName":display_name
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/environments",
            auth=self._auth,
            item=body
        )
        return Environment(**resp.body)

    def delete(self, workspace_id:uuid.UUID, environment_id:uuid.UUID) -> FabricResponse:
        """
        Delete Environment

        Deletes a Environment from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            environment_id (uuid.UUID): The ID of the Environment.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete Environment](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/delete-environment?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/environments/{environment_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:uuid.UUID, environment_id:uuid.UUID) -> Environment:
        """
        Get Environment

        Retrieves a Environment from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the Environment.
            environment_id (uuid.UUID): The ID of the Environment to retrieve.

        Returns:
            Environment: The retrieved Environment.

        References:
            - [Get Environment](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/get-environment?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/environments/{environment_id}",
            auth=self._auth
        )
        return Environment(**resp.body)

    def ls(self, workspace_id:uuid.UUID) -> Iterator[Environment]:
            """
            List Environment

            Retrieves a list of Environment associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.

            Yields:
                Iterator[Environment]: An iterator of Environment objects.

            Reference:
                [List Environment](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/list-environments?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/environments",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield Environment(**item)

    def update(self, workspace_id:uuid.UUID, environment_id:uuid.UUID, display_name:str, description:str) -> FabricResponse:
        """
        Update Environment Definition

        This method updates the definition of a Environment in Power BI.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Environment is located.
            environment_id (uuid.UUID): The ID of the Environment to update.
            definition (dict): The updated definition of the Environment.

        Returns:
            Environment: The updated Environment object.

        Reference:
        - [Update Environment Definition](https://learn.microsoft.com/en-us/rest/api/fabric/environment/items/update-environment?tabs=HTTP)
        """
        body = dict()
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        resp = _http._post_http(
            url = f"{self._base_url}workspaces/{workspace_id}/environments/{environment_id}",
            auth=self._auth,
            item=body
        )
        return resp