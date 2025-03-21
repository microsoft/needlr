from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.reflex import Reflex
from needlr.models.item import Item

class _ReflexClient():
    """

    [Reference]()

    ### Coverage

    * Create Reflex > create()
    * Delete Reflex > delete()
    * Get Reflex > get()
    * Get Reflex Definition > get_definition()
    * List Reflexes > ls()
    * Update Reflex > update()
    * Update Reflex Definition > update_definition()
    
    """


    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a new instance of the Reflex class.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL of the Reflex.
        """
        self._auth = auth
        self._base_url = base_url

    def create(self, workspace_id:uuid.UUID, display_name:str, definition: str=None, description:str=None) -> Reflex:
        """
        Create Reflex

        This method creates a Reflex in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Reflex will be created.
            display_name (str): The display name of the Reflex.
            description (str, optional): The description of the Reflex. Defaults to None.

        Returns:
            Reflex: The created Reflex.

        Reference:
        [Create Reflex](https://learn.microsoft.com/en-us/rest/api/fabric/reflex/items/create-reflex?tabs=HTTP)
        """
        body = {
            "displayName":display_name
        }
        
        if definition:
            body["definition"] = definition
        
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/reflexes",
            auth=self._auth,
            item=Reflex(**body)
        )
        reflex = Reflex(**resp.body)
        return reflex
    
    def delete(self, workspace_id:uuid.UUID, reflex_id:uuid.UUID) -> FabricResponse:
        """
        Delete Reflex

        Deletes a Reflex from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            reflex_id (uuid.UUID): The ID of the Reflex.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete Reflex](https://learn.microsoft.com/en-us/rest/api/fabric/reflex/items/delete-reflex?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/reflexes/{reflex_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:uuid.UUID, reflex_id:uuid.UUID) -> Reflex:
        """
        Get Reflex

        Retrieves a Reflex from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the Reflex.
            reflex_id (uuid.UUID): The ID of the Reflex to retrieve.

        Returns:
            Reflex: The retrieved Reflex.

        References:
            - [Get Reflex](https://learn.microsoft.com/en-us/rest/api/fabric/reflex/items/get-reflex?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/reflexes/{reflex_id}",
            auth=self._auth
        )
        reflex = Reflex(**resp.body)
        return reflex
    
    def get_definition(self, workspace_id:uuid.UUID, reflex_id:uuid.UUID, format: str) -> dict:
        """
        Get Reflex Definition

        Retrieves the definition of a reflex for a given workspace and reflex ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            reflex_id (uuid.UUID): The ID of the reflex.

        Returns:
            dict: The definition of the reflex.

        Raises:
            SomeException: If there is an error retrieving the reflex definition.

        Reference:
        - [Get Reflex Definition](https://learn.microsoft.com/en-us/rest/api/fabric/reflex/items/get-reflex-definition?tabs=HTTP)
        """

        flag = f'?format={format}' if format else ''
        try:
            resp = _http._post_http_long_running(
                url = f"{self._base_url}workspaces/{workspace_id}/reflexes/{reflex_id}/getDefinition{flag}",
                auth=self._auth
            )
            if resp.is_successful:
                return resp.body['definition']
            else:
                return None
        except Exception:
             raise Exception("Error getting reflex definition")

    def ls(self, workspace_id:uuid.UUID, continuation_token: str) -> Iterator[Reflex]:
            """
            List Reflex

            Retrieves a list of Reflexes associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.
                continuation_token (str, optional): A token for retrieving the next page of results.

            Yields:
                Iterator[Reflex]: An iterator of Reflex objects.

            Reference:
                [List Reflexes](https://learn.microsoft.com/en-us/rest/api/fabric/reflex/items/list-reflexes?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/reflexes",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield Reflex(**item)

    def update(self, workspace_id:uuid.UUID, reflex_id:uuid.UUID) -> Reflex:
        """
        Update Reflex

        This method updates the definition of a Reflex in Fabric.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Reflex is located.
            reflex_id (uuid.UUID): The ID of the Reflex to update.

        Returns:
            Reflex: The updated Reflex object.

        Reference:
        - [Update Reflex](https://learn.microsoft.com/en-us/rest/api/fabric/reflex/items/update-reflex?tabs=HTTP)
        """
        body = dict()

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/reflexes/{reflex_id}",
            auth=self._auth,
            item=Item(**body)
        )
        return resp

    def update_definition(self, workspace_id:uuid.UUID, reflex_id:uuid.UUID, definition:dict, updateMetadata:bool = False) -> Reflex:
            """
            Update Reflex Definition
            
            This method updates the definition of a reflex for a given workspace and reflex ID.
            
            Args:
                workspace_id (uuid.UUID): The ID of the workspace.
                reflex_id (uuid.UUID): The ID of the reflex.
                definition (dict): The new definition for the reflex.

            Returns:
                Reflex: The updated reflex object.

            Raises:
                SomeException: If there is an error updating the reflex definition. 

            Reference:
            - [Update Reflex Definition](https://learn.microsoft.com/en-us/rest/api/fabric/reflex/items/update-reflex-definition?tabs=HTTP)
            """

            flag = f'?updateMetadata={updateMetadata}' if updateMetadata else ''
            try:
                resp = _http._post_http_long_running(
                    url = f"{self._base_url}workspaces/{workspace_id}/reflexes/{reflex_id}/updateDefinition{flag}",
                    auth=self._auth,
                    json_par=definition
                )
                if resp.is_successful:
                    return self.get(workspace_id, reflex_id, include_definition=True)
                else:
                        return None
            except Exception:
                    raise Exception("Error updating reflex definition")