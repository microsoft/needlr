"""Module providing Core Pipelines functions."""

from collections.abc import Iterator
import uuid
import json

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.datapipeline import Datapipeline
from needlr.models.item import Item


class _DatapipelineClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/datapipeline/items)

    ### Coverage

    * Create Datapipeline > create()
    * Delete Datapipeline > delete()
    * Get Datapipeline > get()
    * Get Datapipeline Definition > get_definition()
    * List Datapipelines > ls()
    * Update Datapipeline > update()
    * Update Datapipeline Definition > update_definition()
    * Clone Datapipeline > clone()
    * Run on-demand item job > run_on_demand_job()
    * Get Item Job Instance > get_item_job_instance()

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

    def create(self, workspace_id:uuid.UUID, display_name:str, description:str=None, definition:dict=None ) -> Datapipeline:
        """
        Create Datapipeline

        This method creates a Datapipeline in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Datapipeline will be created.
            display_name (str): The display name of the Datapipeline.
            description (str, optional): The description of the Datapipeline. Defaults to None.
            definition (dict): The definition of the Datapipeline. . Defaults to None.

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
        if definition:
            body["definition"] = definition

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/dataPipelines",
            auth=self._auth,
            item=Datapipeline(**body)
        )
        datapipeline = Datapipeline(**resp.body)
        datapipeline.definition = definition
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
    
    def get(self, workspace_id:uuid.UUID, datapipeline_id:uuid.UUID, include_definition:bool = False) -> Datapipeline:
        """
        Get Datapipeline

        Retrieves a Datapipeline from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the Datapipeline.
            datapipeline_id (uuid.UUID): The ID of the Datapipeline to retrieve.
            include_definition (bool, optional): Specifies whether to include the definition of the Datapipeline. 
                Defaults to False.

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
        if include_definition:
            definition = self.get_definition(workspace_id, datapipeline_id)
            datapipeline.definition = definition
        return datapipeline

    def get_definition(self, workspace_id:uuid.UUID, datapipeline_id:uuid.UUID) -> dict:
        """
        Get Datapipeline Definition

        Retrieves the definition of a Datapipeline for a given workspace and Datapipeline ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            datapipeline_id (uuid.UUID): The ID of the Datapipeline.

        Returns:
            dict: The definition of the Datapipeline.

        Raises:
            SomeException: If there is an error retrieving the Datapipeline definition.

        Reference:
        - [Get Datapipeline Definition](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-rest-api#get-item-definition)
        """
        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/items/{datapipeline_id}/getDefinition",
            auth=self._auth
        )
        return resp.body['definition']

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
        Update  Datapipeline

        This method updates the definition of a  Datapipeline in Fabric.

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

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/dataPipelines/{datapipeline_id}",
            auth=self._auth,
            item=Item(**body)
        )
        return resp

    def update_definition(self, workspace_id:uuid.UUID, datapipeline_id:uuid.UUID, definition:dict) -> FabricResponse:
        """
        Update Datapipeline Definition

        This method updates the definition of a Datapipeline in Fabric.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Report is located.
            datapipeline_id (uuid.UUID): The ID of the Report to update.
            definition (dict): The updated definition of the Datapipeline.

        Returns:
            Datapipeline: The updated Datapipeline object.

        Reference:
        - [Update Datapipeline Definition](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-rest-api#update-item-definition)
        """

        body = {
            "displayName":"N/A",
            "definition":definition
        }
        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/items/{datapipeline_id}/updateDefinition",
            auth=self._auth,
            item=Item(**body)
        )
        return resp

    def clone(self, source_workspace_id:uuid.UUID, datapipeline_id:uuid.UUID, clone_name:str, target_workspace_id:uuid.UUID) -> Datapipeline:
        """
        Clone Datapipeline

        This method clones a Datapipeline from one workspace to another.

        Args:
            source_workspace_id (uuid.UUID): The ID of the source workspace.
            datapipeline_id (uuid.UUID): The ID of the Datapipeline to clone.
            clone_name (str): The name of the cloned Datapipeline.
            target_workspace_id (uuid.UUID): The ID of the target workspace.

        Returns:
            Datapipeline: The cloned Datapipeline.

        Reference:
            [Clone Datapipeline](https://learn.microsoft.com/en-us/rest/api/fabric/datapipeline/items/clone-data-pipeline?tabs=HTTP)
        """
        source_datapipeline = self.get(source_workspace_id, datapipeline_id , include_definition=True)
        if target_workspace_id is None:
            target_workspace_id = source_workspace_id
        cloned_datapipeline =  self.create(target_workspace_id, display_name=clone_name, 
                                           definition=source_datapipeline.definition, description=source_datapipeline.description)
        return cloned_datapipeline

    def run_on_demand_job(self, workspace_id:uuid.UUID, datapipeline_id:uuid.UUID, parameters:json = None) -> uuid.UUID:
        """
        Run on-demand item job

        This method runs an on-demand job for a Datapipeline.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            datapipeline_id (uuid.UUID): The ID of the Datapipeline.
            parameters (json): The parameters for the on-demand job.

        Returns:
            Job ID: The job id returned from the on-demand job request.

        Reference:
            [Run on-demand item job](https://learn.microsoft.com/en-us/rest/api/fabric/datapipeline/items/run-on-demand-job?tabs=HTTP)
        """
        resp = _http._post_http(
            url = f"{self._base_url}workspaces/{workspace_id}/items/{datapipeline_id}/jobs/instances?jobType=Pipeline",
            auth=self._auth,
            json=parameters
        )
        if resp.is_successful:
            # There is no body returned currently, but the job Id should be returned. 
            # During the preview, it can be found in the returned headers, in the ‘Location’ property.
            return resp.next_location.split( '/')[-1]
        else:
            return None
    
    def get_item_job_instance(self, workspace_id:uuid.UUID, datapipeline_id:uuid.UUID, job_instance_id:uuid.UUID) -> FabricResponse:
        """
        Get Item Job Instance

        This method retrieves the status of an item job instance.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            datapipeline_id (uuid.UUID): The ID of the Datapipeline.
            job_instance_id (uuid.UUID): The ID of the job instance.

        Returns:
            FabricResponse: The response from the get item job instance request.

        Reference:
            [Get Item Job Instance](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-rest-api#get-item-job-instance)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/items/{datapipeline_id}/jobs/instances/{job_instance_id}",
            auth=self._auth
        )
        return resp.body

    def cancel_item_job_instance(self, workspace_id:uuid.UUID, datapipeline_id:uuid.UUID, job_instance_id:uuid.UUID) -> FabricResponse:
        """
        Cancel Item Job Instance

        This method cancels an item job instance.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            datapipeline_id (uuid.UUID): The ID of the Datapipeline.
            job_instance_id (uuid.UUID): The ID of the job instance.

        Returns:
            FabricResponse: The response from the cancel item job instance request.

        Reference:
            [Cancel Item Job Instance](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-rest-api#cancel-item-job-instance)
        """
        resp = _http._post_http(
            url = f"{self._base_url}workspaces/{workspace_id}/items/{datapipeline_id}/jobs/instances/{job_instance_id}/cancel",
            auth=self._auth
        )
        return resp
    
    def query_activity_runs(self, workspace_id:uuid.UUID, job_id:uuid.UUID, parameters:json) -> FabricResponse:
        """
        Query Activity Runs

        This method queries the activity runs for a specific job in a Workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace
            job_id (uuid.UUID): The ID of the job.
            parameters (json): The parameters for the query. For example
                {
                "filters":[],
                "orderBy":[{"orderBy":"ActivityRunStart","order":"DESC"}],
                "lastUpdatedAfter":"2024-05-22T14:02:04.1423888Z",
                "lastUpdatedBefore":"2024-05-24T13:21:27.738Z"
                }

        Returns:
            FabricResponse: The response from the query activity runs request.

        Reference:
            [Query Activity Runs](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-rest-api#query-activity-runs)
        """
        resp = _http._post_http(
            url = f"{self._base_url}workspaces/{workspace_id}/datapipelines/pipelineruns/{job_id}/queryactivityruns",
            auth=self._auth,
            json=parameters
        )
        return resp.body
