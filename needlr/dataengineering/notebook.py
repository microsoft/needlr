from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.notebook import Notebook

class _NotebookClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items)

    ### Coverage

    * Create Notebook > create()
    * Delete Notebook > delete()
    * Get Notebook > get()
    * Get Notebook Definition > get_definition()
    * List Notebooks > ls()
    * Update Notebooks > update()
    * Update Notebook Definition > update_definition()

    """
    def __init__(self, auth:_FabricAuthentication, base_url:str):
        """
        Initializes a Notebook client to support, get, update, delete operations on notebooks.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the notebook.

        """        
        self._auth = auth
        self._base_url = base_url

    def create(self, display_name:str, workspace_id:uuid.UUID, description:str=None) -> Notebook:
        """
        Creates a notebook in the specified workspace.
        This API supports long running operations (LRO).

        Args:
            display_name (str): The display name of the notebook.
            workspace_id (uuid.UUID): The ID of the workspace where the notebook will be created.
            description (str, optional): The description of the notebook. Defaults to None.

        Returns:
            Notebook: The created notebook object.

        Reference:
        - [Create Notebook](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP)
        """
        body = {
            "displayName":display_name
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/notebooks",
            auth=self._auth,
            item=Notebook(**body)
        )
        return Notebook(**resp.body)   

    def get_definition(self, workspace_id:uuid.UUID, notebook_id:uuid.UUID) -> dict:
        """
        Get Notebook Definition

        Retrieves the definition of a notebook for a given workspace and notebook ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            notebook_id (uuid.UUID): The ID of the notebook.

        Returns:
            dict: The definition of the notebook.

        Raises:
            SomeException: If there is an error retrieving the notebook definition.

        Reference:
        - [Get Semantic Model Definition](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/get-semantic-model-definition?tabs=HTTP)
        """
        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/notebooks/{notebook_id}/getDefinition",
            auth=self._auth
        )
        return resp.body['definition']    
    
    def get(self, workspace_id:uuid.UUID, notebook_id:uuid.UUID, include_definition:bool = False) -> Notebook:
        """
        Get a Notebook

        Returns the meta-data/properties of the specified notebook.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            notebook_id (uuid.UUID): The ID of the notebook.
            include_definition (bool, optional): Specifies whether to include the definition of the Notebook. 
                Defaults to False.

        Returns:
            Notebook: The retrieved notebook object.

        Reference:
        [Get Notebook](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/get-notebook?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/notebooks/{notebook_id}",
            auth=self._auth
        )
        notebook = Notebook(**resp.body)
        if include_definition:
            definition = self.get_definition(workspace_id, notebook_id)
            notebook.definition = definition
        return notebook
    
    def ls(self, workspace_id:uuid.UUID) -> Iterator[Notebook]:

        """
        List Notebooks

        This method retrieves a list of notebooks associated with the specified workspace ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.

        Returns:
            Iterator[Notebook]: An iterator that yields Notebook objects.

        Reference:
        - [List Notebooks](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/list-notebooks?tabs=HTTP)
        """
        resp = _http._get_http_paged(
            url = f"{self._base_url}workspaces/{workspace_id}/notebooks",
            auth=self._auth,
            items_extract=lambda x:x["value"]
        )
        for page in resp:
            for item in page.items:
                yield Notebook(**item)    

    def update(self, workspace_id:uuid.UUID, notebook_id:uuid.UUID, display_name:str=None, description:str=None) -> Notebook:
        """
        Updates the properties of the specified notebook

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the notebook.
            notebook_id (uuid.UUID): The ID of the notebook to update.
            display_name (str, optional): The notebook display name. The display name must follow naming rules according to item type.
            description (str, optional): The notebook description. Maximum length is 256 characters.

        Returns:
            Notebook: The updated notebook object.
        Raises:
            ValueError: If both `display_name` and `description` are left blank.

        Reference:
            [Microsoft Docs](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/update-notebook?tabs=HTTP)
        """
        if ((display_name is None) and (description is None)):
            raise ValueError("display_name or description must be provided")

        body = dict()
        if display_name:
            body["displayName"] = display_name
        if description:
            body["description"] = description

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/notebooks/{notebook_id}",
            auth=self._auth,
            json=body
        )
        notebook = Notebook(**resp.body)
        return notebook
    
    def update_definition(self, workspace_id:uuid.UUID, notebook_id:uuid.UUID, definition:dict, updateMetadata:bool = False) -> Notebook:
            """
            Update Notebook Definition
            Updates the definition of a notebook for a given workspace and notebook ID.
            Args:
                workspace_id (uuid.UUID): The ID of the workspace.
                notebook_id (uuid.UUID): The ID of the notebook.
                definition (dict): The new definition for the notebook.
                    Sample definition (reading from file):
                     "definition": {
                            "parts": [
                                {
                                    "path": "notebook-content.py",
                                    "payload": base64.b64encode(open('part0.txt', 'rb').read()).decode('utf-8'),
                                    "payloadType": "InlineBase64"
                                },
                                {
                                    "path": ".platform",
                                    "payload": base64.b64encode(open('part1.txt', 'rb').read()).decode('utf-8'),
                                    "payloadType": "InlineBase64"
                                }
                            ]
                        }
            Returns:
                Notebook: The updated notebook object.
            Raises:
                SomeException: If there is an error updating the notebook definition.   
            Reference:
            - [Update Notebook Definition](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/update-notebook-definition?tabs=HTTP)
            """
            flag = f'?updateMetadata={updateMetadata}' if updateMetadata else ''
            try:
                resp = _http._post_http_long_running(
                    url = f"{self._base_url}workspaces/{workspace_id}/notebooks/{notebook_id}/updateDefinition{flag}",
                    auth=self._auth,
                    json_par=definition
                )
                if resp.is_successful:
                    return self.get(workspace_id, notebook_id, include_definition=True)
                else:
                        return None
            except Exception:
                    raise Exception("Error updating notebook definition")

    def delete(self, workspace_id:uuid.UUID, notebook_id:uuid.UUID) -> FabricResponse:
        """
        Delete a notebook.

        Deletes a notebook for the specified `notebook_id` in the given `workspace_id`.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            notebook_id (uuid.UUID): The ID of the notebook to be deleted.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
        - [Delete Notebook](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/delete-notebook?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/notebooks/{notebook_id}",
            auth=self._auth
        )
        return resp
    