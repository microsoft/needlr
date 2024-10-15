"""Module providing Notebook functions."""

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
    * List Notebooks > ls()
    * Update Notebooks > update()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a Notebook object.

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
            display_name (str): The display name of the warehouse.
            workspace_id (uuid.UUID): The ID of the workspace where the warehouse will be created.
            description (str, optional): The description of the warehouse. Defaults to None.

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