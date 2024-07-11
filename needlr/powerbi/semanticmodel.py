"""Module providing Core Semantic Model functions."""

from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.semanticmodel import SemanticModel



class _SemanticModelClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items)

    ### Coverage

    * Create Semantic Model > create()
    * Delete Semantic Model > delete()
    * Get Semantic Model > get()
    * Get Semantic Model Definition > get_definition()
    * List Semantic Model > ls()
    * Update Semantic Model > update()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        self._auth = auth
        self._base_url = base_url

    def ls(self, workspace_id:uuid.UUID) -> Iterator[SemanticModel]:
        """
        List Semantic Models

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/list-semantic-models?tabs=HTTP)
        """
        resp = _http._get_http_paged(
            url = f"{self._base_url}workspaces/{workspace_id}/semanticModels",
            auth=self._auth,
            items_extract=lambda x:x["value"]
        )
        for page in resp:
            for item in page.items:
                yield SemanticModel(**item)

    def get(self, workspace_id:uuid.UUID, semanticmodel_id:uuid.UUID) -> SemanticModel:
        """
        Get Semantic Model

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/get-semantic-model?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/semanticModels/{semanticmodel_id}",
            auth=self._auth
        )
        semanticmodel = SemanticModel(**resp.body)
        return semanticmodel

    def delete(self, workspace_id:uuid.UUID, semanticmodel_id:uuid.UUID) -> FabricResponse:
        """
        Delete Warehouse

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/delete-warehouse?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/semanticModels/{semanticmodel_id}",
            auth=self._auth
        )
        return resp
    
    #TODO: It does not work
    def get_definition(self, workspace_id:uuid.UUID, semanticmodel_id:uuid.UUID):
        """
        Get Semantic Model Definition

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/get-semantic-model-definition?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/semanticModels/{semanticmodel_id}/getDefinition",
            auth=self._auth
        )
        return resp.body

    #TODO: Update to use long running operations so I always receive a Semantic Model instead of a response
    def create(self, workspace_id:uuid.UUID, semanticmodel:SemanticModel) -> SemanticModel:
        """
        Create Semantic Model

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/create-semantic-model?tabs=HTTP)
        """
        resp = _http._post_http(
            url = f"{self._base_url}workspaces/{workspace_id}/semanticModels",
            auth=self._auth,
            json=semanticmodel.to_dict()
        )
        semanticmodel = SemanticModel(**resp.body)
        return semanticmodel

    #TODO: Update to use long running operations so I always receive a Semantic Model instead of a response
    def update(self, workspace_id:uuid.UUID, semanticmodel_id:uuid.UUID, semanticmodel:SemanticModel) -> SemanticModel:
        """
        Update Semantic Model

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/update-semantic-model?tabs=HTTP)
        """
        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/semanticModels/{semanticmodel_id}",
            auth=self._auth,
            json=semanticmodel.to_dict()
        )
        semanticmodel = SemanticModel(**resp.body)
        return semanticmodel