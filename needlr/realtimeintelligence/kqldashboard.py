from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.kqldashboard import KQLDashboard
from needlr.models.item import Item

class _KQLDashboardClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/kqldashboard/items)

    ### Coverage

    * Create KQL Dashboard > create()
    * Delete KQL Dashboard > delete()
    * Get KQL Dashboard > get()
    * Get KQL Dashboard Definition > get_definition()
    * List KQL Dashboards > ls()
    * Update KQL Dashboard > update()
    * Update KQL Dashboard Definition > update_definition()
    
    """

    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a new instance of the KQLDashboard class.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL of the KQL Dashboard.
        """
        self._auth = auth
        self._base_url = base_url

    def create(self, workspace_id:uuid.UUID, display_name:str, definition: str=None, description:str=None) -> KQLDashboard:
        """
        Create KQL Dashboard

        This method creates a KQL Dashboard in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Reflex will be created.
            display_name (str): The display name of the KQL Dashboard.
            definition (str, optional): The KQL dashboard description. Maximum length is 256 characters.
            description (str, optional): The description of the KQL Dashboard. Defaults to None.
            

        Returns:
            KQLDashboard: The created KQL Dashboard.

        Reference:
        [Create KQL Dashboard]https://learn.microsoft.com/en-us/rest/api/fabric/kqldashboard/items/create-kql-dashboard?tabs=HTTP()
        """
        body = {
            "displayName":display_name
        }
        
        if definition:
            body["definition"] = definition
        
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlDashboards",
            auth=self._auth,
            item=KQLDashboard(**body)
        )
        kqlDashboard = KQLDashboard(**resp.body)
        return kqlDashboard
    
    def delete(self, workspace_id:uuid.UUID, kqlDashboard_id:uuid.UUID) -> FabricResponse:
        """
        Delete KQL Dashboard

        Deletes a KQL Dashboard from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            kqldashboard_id (uuid.UUID): The ID of the KQL Dashboard.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete KQL Dashboard](https://learn.microsoft.com/en-us/rest/api/fabric/kqldashboard/items/delete-kql-dashboard?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlDashboards/{kqlDashboard_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:uuid.UUID, kqlDashboard_id:uuid.UUID) -> KQLDashboard:
        """
        Get KQL Dashboard

        Retrieves a KQL Dashboard from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the KQL Dashboard.
            kqldashboard_id (uuid.UUID): The ID of the KQL Dashboard to retrieve.

        Returns:
            KQLDashboard: The retrieved KQL Dashboard.

        References:
            - [Get KQL Dashboard](https://learn.microsoft.com/en-us/rest/api/fabric/kqldashboard/items/get-kql-dashboard?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlDashboards/{kqlDashboard_id}",
            auth=self._auth
        )
        kqlDashboard = KQLDashboard(**resp.body)
        return kqlDashboard

    def get_definition(self, workspace_id:uuid.UUID, kqlDashboard_id:uuid.UUID, format: str=None) -> dict:
        """
        Get KQL Dashboard Definition

        Retrieves the definition of a KQL Dashboard for a given workspace and KQL Dashboard ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            kqldashboard_id (uuid.UUID): The ID of the KQL Dashboard.
            format (str, optional): The format of the KQL Dashboard public definition.

        Returns:
            dict: The definition of the KQL Dashboard.

        Raises:
            SomeException: If there is an error retrieving the KQL Dashboard definition.

        Reference:
        - [Get KQL Dashboard Definition](https://learn.microsoft.com/en-us/rest/api/fabric/kqldashboard/items/get-kql-dashboard-definition?tabs=HTTP)
        """

        flag = f'?format={format}' if format else ''
        try:
            resp = _http._post_http_long_running(
                url = f"{self._base_url}workspaces/{workspace_id}/kqlDashboards/{kqlDashboard_id}/getDefinition{flag}",
                auth=self._auth
            )
            if resp.is_successful:
                return resp.body['definition']
            else:
                return None
        except Exception:
             raise Exception("Error getting KQL Dashboard definition")

    def ls(self, workspace_id:uuid.UUID, continuation_token: str=None) -> Iterator[KQLDashboard]:
            """
            List KQL Dashboards

            Retrieves a list of KQL Dashboards associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.
                continuation_token (str, optional): A token for retrieving the next page of results.

            Yields:
                Iterator[KQLDashboard]: An iterator of KQL Dashboard objects.

            Reference:
                [List KQL Dashboards](https://learn.microsoft.com/en-us/rest/api/fabric/kqldashboard/items/list-kql-dashboards?tabs=HTTP)
            """
            flag = f'?continuationToken={continuation_token}' if continuation_token else ''
            resp = _http._get_http_paged(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlDashboards{flag}",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield KQLDashboard(**item)

    def update(self, workspace_id:uuid.UUID, kqlDashboard_id:uuid.UUID) -> KQLDashboard:
        """
        Update KQL Dashboard

        This method updates the definition of a KQL Dashboard in Fabric.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the KQL Dashboard is located.
            kqldashboard_id (uuid.UUID): The ID of the KQL Dashboard to update.

        Returns:
            KQLDashboard: The updated KQL Dashboard object.

        Reference:
        - [Update KQL Dashboard](https://learn.microsoft.com/en-us/rest/api/fabric/kqldashboard/items/update-kql-dashboard?tabs=HTTP)
        """
        body = dict()

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlDashboards/{kqlDashboard_id}",
            auth=self._auth,
            item=Item(**body)
        )
        return resp
    
    def update_definition(self, workspace_id:uuid.UUID, kqlDashboard_id:uuid.UUID, definition:dict, updateMetadata:bool = False) -> KQLDashboard:
            """
            Update KQL Dashboard Definition
            
            This method updates the definition of a KQL Dashboard for a given workspace and KQL Dashboard ID.
            
            Args:
                workspace_id (uuid.UUID): The ID of the workspace.
                kqldashboard_id (uuid.UUID): The ID of the KQL Dashboard.
                definition (dict): The new definition for the KQL Dashboard.
                updateMetadata (boolean, optional): If set to true, the item's metadata is updated.

            Returns:
                KQLDashboard: The updated KQL Dashboard object.

            Raises:
                SomeException: If there is an error updating the KQL Dashboard definition. 

            Reference:
            - [Update KQL Dashboard Definition](https://learn.microsoft.com/en-us/rest/api/fabric/kqldashboard/items/update-kql-dashboard-definition?tabs=HTTP)
            """

            flag = f'?updateMetadata={updateMetadata}' if updateMetadata else ''
            try:
                resp = _http._post_http_long_running(
                    url = f"{self._base_url}workspaces/{workspace_id}/kqlDashboards/{kqlDashboard_id}/updateDefinition{flag}",
                    auth=self._auth,
                    json_par=definition
                )
                if resp.is_successful:
                    return self.get(workspace_id, kqlDashboard_id, include_definition=True)
                else:
                        return None
            except Exception:
                    raise Exception("Error updating KQL Dashboard definition")