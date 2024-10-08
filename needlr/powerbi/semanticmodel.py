"""Module providing Core Semantic Model functions."""

from typing import Optional
from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.semanticmodel import SemanticModel
from needlr.models.item import Item



class _SemanticModelClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items)

    ### Coverage

    * Create Semantic Model > create()
    * Delete Semantic Model > delete()
    * Get Semantic Model > get()
    * Get Semantic Model Definition > get_definition()
    * List Semantic Model > ls()
    * Update Semantic Model Definition > update_definition()
    * Clone Semantic Model > clone()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a SemanticModel object.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL for the SemanticModel.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def ls(self, workspace_id:uuid.UUID) -> Iterator[SemanticModel]:
            """
            List Semantic Models

            Retrieves a list of semantic models associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.

            Yields:
                Iterator[SemanticModel]: An iterator of SemanticModel objects.

            Reference:
                [List Semantic Models](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/list-semantic-models?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/semanticModels",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield SemanticModel(**item)

    def get(self, workspace_id:uuid.UUID, semanticmodel_id:uuid.UUID, include_defintion:bool = False) -> SemanticModel:
        """
        Get Semantic Model

        Retrieves a semantic model from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the semantic model.
            semanticmodel_id (uuid.UUID): The ID of the semantic model to retrieve.
            include_defintion (bool, optional): Specifies whether to include the definition of the semantic model. 
                Defaults to False.

        Returns:
            SemanticModel: The retrieved semantic model.

        References:
            - [Get Semantic Model](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/get-semantic-model?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/semanticModels/{semanticmodel_id}",
            auth=self._auth
        )
        semanticmodel = SemanticModel(**resp.body)
        if include_defintion:
            definition = self.get_definition(workspace_id, semanticmodel_id)
            semanticmodel.definition = definition
        return semanticmodel

    def delete(self, workspace_id:uuid.UUID, semanticmodel_id:uuid.UUID) -> FabricResponse:
        """
        Delete Semantic Model

        Deletes a semantic model from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            semanticmodel_id (uuid.UUID): The ID of the semantic model.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete Semantic Model](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/delete-semantic-model?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/semanticModels/{semanticmodel_id}",
            auth=self._auth
        )
        return resp
    
    def get_definition(self, workspace_id:uuid.UUID, semanticmodel_id:uuid.UUID) -> dict:
        """
        Get Semantic Model Definition

        Retrieves the definition of a semantic model for a given workspace and semantic model ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            semanticmodel_id (uuid.UUID): The ID of the semantic model.

        Returns:
            dict: The definition of the semantic model.

        Raises:
            SomeException: If there is an error retrieving the semantic model definition.

        Reference:
        - [Get Semantic Model Definition](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/get-semantic-model-definition?tabs=HTTP)
        """
        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/semanticModels/{semanticmodel_id}/getDefinition",
            auth=self._auth
        )
        return resp.body['definition']

    def create(self, workspace_id:uuid.UUID, display_name:str, definition:dict, description:str=None) -> SemanticModel:
        """
        Create Semantic Model

        This method creates a semantic model in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the semantic model will be created.
            display_name (str): The display name of the semantic model.
            definition (dict): The definition of the semantic model.
            description (str, optional): The description of the semantic model. Defaults to None.

        Returns:
            SemanticModel: The created semantic model.

        Reference:
        [Create Semantic Model](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/create-semantic-model?tabs=HTTP)
        """
        body = {
            "displayName":display_name,
            "definition":definition
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/semanticModels",
            auth=self._auth,
            item=SemanticModel(**body)
        )
        semanticmodel = SemanticModel(**resp.body)
        semanticmodel.definition = definition
        return semanticmodel

    def update_definition(self, workspace_id:uuid.UUID, semanticmodel_id:uuid.UUID, definition:dict) -> FabricResponse:
        """
        Update Semantic Model

        This method updates the definition of a semantic model in Power BI.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the semantic model is located.
            semanticmodel_id (uuid.UUID): The ID of the semantic model to update.
            definition (dict): The updated definition of the semantic model.

        Returns:
            SemanticModel: The updated semantic model object.

        Reference:
        - [Update Semantic Model Definition](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/update-semantic-model-definition?tabs=HTTP)
        """
        body = {
            "displayName":"N/A",
            "definition":definition
        }

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/semanticModels/{semanticmodel_id}/updateDefinition",
            auth=self._auth,
            item=Item(**body)
        )
        return resp

    def clone(self, source_workspace_id: uuid.UUID, semanticmodel_id: uuid.UUID, clone_name: str,  target_workspace_id: Optional[uuid.UUID]) -> SemanticModel:
        """
        Clones a semantic model.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            semanticmodel_id (uuid.UUID): The ID of the semantic model to clone.
            clone_name (str): The name of the cloned semantic model.

        Returns:
            SemanticModel: The cloned semantic model.
        """
        source_semantic_model = self.get(source_workspace_id, semanticmodel_id, include_defintion=True)
        if target_workspace_id is None:
            target_workspace_id = source_workspace_id
        return self.create(target_workspace_id, display_name=clone_name, definition=source_semantic_model.definition, description=source_semantic_model.description)

