from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.notebook import SparkJobDefinition, SparkJobDefinitionPublicDefinition

class _SparkJobDefinitionClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items)

    ### Coverage

    * Create Spark Definition > create()
    * Delete Spark Definition > delete()
    * Get Spark Definition > get()
    * Get Spark Definition Public Definition > get_public_definition()
    * List Spark Definition > ls()
    * Update Spark Definition > update()
    * Update Spark Definition Public Definition > update_public_definition()
    """
    def __init__(self, auth:_FabricAuthentication, base_url:str):
        """
        Initializes a SparkJobDefinition client to support create, get, update, delete operations on spark job definitions.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the notebook.

        """        
        self._auth = auth
        self._base_url = base_url
    
    def create(self, workspace_id:uuid.UUID, display_name:str, description:str=None, 
               definition:SparkJobDefinitionPublicDefinition=None) -> SparkJobDefinition:
        """
        Creates a spark job definition in the specified workspace.
        This API supports long running operations (LRO).

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the notebook will be created.
            display_name (str): The display name of the notebook.
            description (str, optional): The description of the notebook. Defaults to None.
            definition (SparkJobDefinitionPublicDefinition, optional): The spark job definition. Defaults to None.

        Returns:
            SparkJobDefinition: The created Spark Job Definition object.

        Reference:
        - [Create Spark Job Definition](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/create-spark-job-definition?tabs=HTTP)
        """
        body = {
            "displayName":display_name
        }

        if description:
            body["description"] = description

        if definition:
            body["definition"] = definition
        
        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/sparkJobDefinitions",
            auth=self._auth,
            item=body
        )
        return SparkJobDefinition(**resp.body)
    
    def delete(self, workspace_id:uuid.UUID, spark_job_definition_id:uuid.UUID) -> FabricResponse:
        """
        Delete a Spark Job Definition.

        Deletes a Spark Job Definition for the specified `spark_job_definition_id` in the given `workspace_id`.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            spark_job_definition_id (uuid.UUID): The ID of the Spark Job Definition to be deleted.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
        - [Delete Spark Job Definition](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/delete-spark-job-definition?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:uuid.UUID, spark_job_definition_id:uuid.UUID) -> SparkJobDefinition:
        """
        Get a Spark Job Definition

        Returns the meta-data/properties of the specified Spark Job Definition.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            spark_job_definition_id (uuid.UUID): The ID of the spark job definition.

        Returns:
            SparkJobDefinition: The retrieved spark job definition object.

        Reference:
        [Get Spark Job Definition](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/get-spark-job-definition?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}",
            auth=self._auth
        )

        return SparkJobDefinition(**resp.body)  
    
    def get_public_definition(self, workspace_id:uuid.UUID, spark_job_definition_id:uuid.UUID, format:str=None) -> SparkJobDefinitionPublicDefinition:
        """
        Get a Spark Job Definition

        Returns the meta-data/properties of the specified Spark Job Definition.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            spark_job_definition_id (uuid.UUID): The ID of the spark job definition.
            format  (str): The format of the spark job definition public definition.

        Returns:
            SparkJobDefinitionPublicDefinition: The retrieved spark job definition public definition object.

        Reference:
        [Get Spark Job Definition](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/get-spark-job-definition?tabs=HTTP)
        """
        querystring = None

        if format:
            querystring = f"format={format}"

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}/getDefinition?{querystring}",
            auth=self._auth
        )

        return SparkJobDefinitionPublicDefinition(**resp.body["definition"])  

    def ls(self, workspace_id:uuid.UUID) -> Iterator[SparkJobDefinition]:

        """
        List Spark Job Definition

        This method retrieves a list of Spark Job Definitions associated with the specified workspace ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.

        Returns:
            Iterator[Notebook]: An iterator that yields Spark Job Definition objects.

        Reference:
        - [List Spark Job Definition](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/list-spark-job-definitions?tabs=HTTP)
        """
        resp = _http._get_http_paged(
            url = f"{self._base_url}workspaces/{workspace_id}/sparkJobDefinitions",
            auth=self._auth,
            items_extract=lambda x:x["value"]
        )
        for page in resp:
            for item in page.items:
                yield SparkJobDefinition(**item) 
    
    def update(self, workspace_id:uuid.UUID, spark_job_definition_id:uuid.UUID, display_name:str=None, description:str=None) -> SparkJobDefinition:
        """
        Updates the properties of the specified Spark Job Definition

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the Spark Job Definition.
            spark_job_definition_id (uuid.UUID): The ID of the Spark Job Definition to update.
            display_name (str, optional): The Spark Job Definition display name. The display name must follow naming rules according to item type.
            description (str, optional): The Spark Job Definition description. Maximum length is 256 characters.

        Returns:
            SparkJobDefinition: The updated Spark Job Definition object.

        Raises:
            ValueError: If both `display_name` and `description` are left blank.

        Reference:
            [Update Spark Job Definition](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/update-spark-job-definition?tabs=HTTP)
        """
        if ((display_name is None) and (description is None)):
            raise ValueError("display_name or description must be provided")

        body = dict()
        if display_name:
            body["displayName"] = display_name
        if description:
            body["description"] = description

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}",
            auth=self._auth,
            json=body
        )
        
        return SparkJobDefinition(**resp.body)

    def update_public_definition(self, workspace_id:uuid.UUID, spark_job_definition_id:uuid.UUID, 
                                 definition:SparkJobDefinitionPublicDefinition, update_metatdate:bool=False) -> FabricResponse:
        """
        Updates the properties of the specified Spark Job Definition

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the Spark Job Definition.
            spark_job_definition_id (uuid.UUID): The ID of the Spark Job Definition to update.
            definition (SparkJobDefinitionPublicDefinition): Spark job definition public definition object.
            update_metatdate (bool, optional): When set to true and the .platform file is provided as part of the definition, 
                the item's metadata is updated using the metadata in the .platform file. Defaults to False.

        Returns:
            FabricResponse: The response from the update public definition request.

        Reference:
            [Update Spark Job Definition Public Definition](https://learn.microsoft.com/en-us/rest/api/fabric/sparkjobdefinition/items/update-spark-job-definition-definition?tabs=HTTP)
        """
        body = {
            "definition":definition
        }

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}/updateDefinition?updateMetadata={update_metatdate}",
            auth=self._auth,
            json=body
        )
        
        return resp