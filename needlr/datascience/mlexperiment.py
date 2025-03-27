from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.mlexperiment import MLExperiment
from needlr.models.item import Item

class _MLExperimentClient():
    """

    [Reference]()

    ### Coverage

    * Create ML Experiment > create()
    * Delete ML Experiment > delete()
    * Get ML Experiment > get()
    * List ML Experiment > ls()
    * Update ML Experiment > update()
    
    """


    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a new instance of the ML Experiment class.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL of the ML Experiment.
        """
        self._auth = auth
        self._base_url = base_url

    def create(self, workspace_id:uuid.UUID, display_name:str, description:str=None) -> MLExperiment:
        """
        Create ML Experiment

        This method creates an MLModel in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the ML Experiment will be created.
            display_name (str): The display name of the ML Experiment.
            description (str, optional): The description of the ML Experiment. Defaults to None.

        Returns:
            MLExperiment: The created ML Experiment.

        Reference:
        [Create ML Experiment](https://learn.microsoft.com/en-us/rest/api/fabric/mlexperiment/items/create-ml-experiment?tabs=HTTP)
        """
        body = {
            "displayName":display_name
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/mlExperiments",
            auth=self._auth,
            item=MLExperiment(**body)
        )
        mlexperiment = MLExperiment(**resp.body)
        return mlexperiment
    
    def delete(self, workspace_id:uuid.UUID, mlexperiment_id:uuid.UUID) -> FabricResponse:
        """
        Delete ML Experiment

        Deletes an ML Experiment from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            mlexperiment_id (uuid.UUID): The ID of the ML Experiment.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete ML Experiment](https://learn.microsoft.com/en-us/rest/api/fabric/mlexperiment/items/delete-ml-experiment?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/mlExperiments/{mlexperiment_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:uuid.UUID, mlexperiment_id:uuid.UUID) -> MLExperiment:
        """
        Get ML Experiment

        Retrieves an ML Experiment from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the ML Experiment.
            mlexperiment_id (uuid.UUID): The ID of the ML Experiment to retrieve.

        Returns:
            MLExperiment: The retrieved ML Experiment.

        References:
            - [Get ML Experiment](https://learn.microsoft.com/en-us/rest/api/fabric/mlexperiment/items/get-ml-experiment?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/mlExperiments/{mlexperiment_id}",
            auth=self._auth
        )
        mlexperiment = MLExperiment(**resp.body)
        return mlexperiment
    
    def ls(self, workspace_id:uuid.UUID, continuation_token: str=None) -> Iterator[MLExperiment]:
            """
            List ML Experiment

            Retrieves a list of ML Experiments associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.
                continuation_token (str, optional): A token for retrieving the next page of results.

            Yields:
                Iterator[MLExperiment]: An iterator of ML Experiment objects.

            Reference:
                [List ML Experiment](https://learn.microsoft.com/en-us/rest/api/fabric/mlexperiment/items/list-ml-experiments?tabs=HTTP)
            """
            flag = f'?continuationToken={continuation_token}' if continuation_token else ''
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/mlExperiments{flag}",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield MLExperiment(**item)

    def update(self, workspace_id:uuid.UUID, mlexperiment_id:uuid.UUID, display_name: str, description: str) -> MLExperiment:
        """
        Update ML Experiment

        This method updates the definition of an ML Experiment in Fabric.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the ML Experiment is located.
            mlexperiment_id (uuid.UUID): The ID of the ML Experiment to update.
            display_name (str): The ML Experiment display name.
            description (str): The ML Experiment description.

        Returns:
            MLExperiment: The updated ML Experiment object.

        Reference:
        - [Update ML Experiment Definition](https://learn.microsoft.com/en-us/rest/api/fabric/mlexperiment/items/update-ml-experiment?tabs=HTTP)
        """
        if ((display_name is None) and (description is None)):
            raise ValueError("display_name or description must be provided")

        body = dict()
        if display_name:
            body["displayName"] = display_name
        if description:
            body["description"] = description

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/mlExperiments/{mlexperiment_id}",
            auth=self._auth,
            json=body
        )
        mlExperiment = MLExperiment(**resp.body)
        return mlExperiment