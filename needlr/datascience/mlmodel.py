from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.mlmodel import MLModel
from needlr.models.item import Item

class _MLModelClient():
    """

    [Reference]()

    ### Coverage

    * Create ML Model > create()
    * Delete ML Model > delete()
    * Get ML Model > get()
    * List ML Models > ls()
    * Update ML Model > update()
    
    """


    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a new instance of the ML Model class.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL of the ML Model.
        """
        self._auth = auth
        self._base_url = base_url

    def create(self, workspace_id:uuid.UUID, display_name:str, description:str=None) -> MLModel:
        """
        Create MLModel

        This method creates an MLModel in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the MLModel will be created.
            display_name (str): The display name of the MLModel.
            description (str, optional): The description of the MLModel. Defaults to None.

        Returns:
            MLModel: The created MLModel.

        Reference:
        [Create MLModel](https://learn.microsoft.com/en-us/rest/api/fabric/mlmodel/items/create-ml-model?tabs=HTTP&tryIt=true#createmlmodelrequest)
        """
        body = {
            "displayName":display_name
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/mlModels",
            auth=self._auth,
            item=MLModel(**body)
        )
        mlmodel = MLModel(**resp.body)
        return mlmodel
    
    def delete(self, workspace_id:uuid.UUID, mlmodel_id:uuid.UUID) -> FabricResponse:
        """
        Delete MLModel

        Deletes an MLModel from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            mlmodel_id (uuid.UUID): The ID of the MLModel.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete MLModel](DELETE https://learn.microsoft.com/en-us/rest/api/fabric/mlmodel/items/delete-ml-model?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/mlModels/{mlmodel_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:uuid.UUID, mlmodel_id:uuid.UUID) -> MLModel:
        """
        Get MLModel

        Retrieves a MLModel from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the ML Model.
            mlmodel_id (uuid.UUID): The ID of the ML Model to retrieve.

        Returns:
            MLModel: The retrieved ML Model.

        References:
            - [Get ML Model](https://learn.microsoft.com/en-us/rest/api/fabric/mlmodel/items/get-ml-model?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/mlModels/{mlmodel_id}",
            auth=self._auth
        )
        mlmodel = MLModel(**resp.body)
        return mlmodel
    
    def ls(self, workspace_id:uuid.UUID, continuation_token: str) -> Iterator[MLModel]:
            """
            List ML Models

            Retrieves a list of ML Models associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.
                continuation_token (str, optional): A token for retrieving the next page of results.

            Yields:
                Iterator[MLModel]: An iterator of ML Model objects.

            Reference:
                [List ML Models](https://learn.microsoft.com/en-us/rest/api/fabric/mlmodel/items/list-ml-models?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/mlModel",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield MLModel(**item)

    def update(self, workspace_id:uuid.UUID, mlmodel_id:uuid.UUID) -> MLModel:
        """
        Update ML Model

        This method updates the definition of an ML Model in Fabric.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the  Datapipeline is located.
            mlmodel_id (uuid.UUID): The ID of the ML Model to update.

        Returns:
            MLModel: The updated ML Model object.

        Reference:
        - [Update ML Model Definition](https://learn.microsoft.com/en-us/rest/api/fabric/mlmodel/items/update-ml-model?tabs=HTTP)
        """
        body = dict()

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/mlModel/{mlmodel_id}",
            auth=self._auth,
            item=Item(**body)
        )
        return resp




    
