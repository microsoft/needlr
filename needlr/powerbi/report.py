"""Module providing a Core Workspace functions."""

from typing import Optional
from collections.abc import Iterator
import uuid

from needlr.core.item.item import _ItemClient
from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.core.workspace.role import _WorkspaceRoleClient
from needlr.models.workspace import Workspace
from needlr.models.report import Report
from needlr.models.item import Item, ItemType


class _ReportClient():
    """

    [Reference]https://learn.microsoft.com/en-us/rest/api/fabric/report/items)

    ### Coverage

    * Create Report > create()
    * Delete Report > delete()
    * Get Report > get()
    * Get Report Definition > get_definition()
    * List Reports > ls()
    * Update Report > update()
    * Update Report Defintion > update_definition()
    * Clone Report > clone()

    """
    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a new instance of the Report class.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL of the Report.

        """
        self._auth = auth
        self._base_url = base_url
        self.item = _ItemClient()
        self.role = _WorkspaceRoleClient(auth, base_url)

    def create(self, workspace_id:uuid.UUID, display_name:str, definition:dict, description:str=None) -> Report:
        """
        Create Report

        This method creates a report in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the report will be created.
            display_name (str): The display name of the report.
            definition (dict): The definition of the report.
            description (str, optional): The description of the report. Defaults to None.

        Returns:
            Report: The created report.

        Reference:
        [Create Report](https://learn.microsoft.com/en-us/rest/api/fabric/report/items/create-report?tabs=HTTP)
        """
        body = {
            "displayName":display_name,
            "definition":definition
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/reports",
            auth=self._auth,
            item=Report(**body)
        )
        report = Report(**resp.body)
        report.definition = definition
        return report

    def delete(self, workspace_id:uuid.UUID, report_id:uuid.UUID) -> FabricResponse:
        """
        Delete Report

        Deletes a Report from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            report_id (uuid.UUID): The ID of the Report.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete Report](DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/reports/{reportId})
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/reports/{report_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:uuid.UUID, report_id:uuid.UUID, include_defintion:bool = False) -> Report:
        """
        Get Report

        Retrieves a Report from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the Report.
            report_id (uuid.UUID): The ID of the Report to retrieve.
            include_defintion (bool, optional): Specifies whether to include the definition of the Report. 
                Defaults to False.

        Returns:
            Report: The retrieved Report.

        References:
            - [Get Report](GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/reports/{reportId})
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/reports/{report_id}",
            auth=self._auth
        )
        report = Report(**resp.body)
        if include_defintion:
            definition = self.get_definition(workspace_id, report_id)
            report.definition = definition
        return report

    def get_definition(self, workspace_id:uuid.UUID, report_id:uuid.UUID) -> dict:
        """
        Get Report Definition

        Retrieves the definition of a Report for a given workspace and Report ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            report_id (uuid.UUID): The ID of the Report.

        Returns:
            dict: The definition of the Report.

        Raises:
            SomeException: If there is an error retrieving the Report definition.

        Reference:
        - [Get Report Definition](https://learn.microsoft.com/en-us/rest/api/fabric/report/items/get-report-definition?tabs=HTTP)
        """
        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/reports/{report_id}/getDefinition",
            auth=self._auth
        )
        return resp.body['definition']

    def ls(self, workspace_id:uuid.UUID) -> Iterator[Report]:
            """
            List Reports

            Retrieves a list of Reports associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.

            Yields:
                Iterator[Report]: An iterator of Report objects.

            Reference:
                [List Reports](https://learn.microsoft.com/en-us/rest/api/fabric/report/items/list-reports?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/reports",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield Report(**item)

    def update(self, workspace_id:uuid.UUID, report_id:uuid.UUID, display_name:str, description:str) -> Report:
        """
        Update  Report Definition

        This method updates the definition of a  Report in Power BI.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the  Report is located.
            report_id (uuid.UUID): The ID of the  Report to update.
            definition (dict): The updated definition of the  Report.

        Returns:
            Report: The updated  report object.

        Reference:
        - [Update  Report Definition]PATCH https://learn.microsoft.com/en-us/rest/api/fabric/report/items/update-report-definition?tabs=HTTP)
        """
        body = dict()
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        resp = _http._post_http(
            url = f"{self._base_url}workspaces/{workspace_id}/reports/{report_id}",
            auth=self._auth,
            item=Item(**body)
        )
        return resp

    def update_definition(self, workspace_id:uuid.UUID, report_id:uuid.UUID, definition:dict) -> FabricResponse:
        """
        Update Report Definition

        This method updates the definition of a Report in Power BI.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Report is located.
            report_id (uuid.UUID): The ID of the Report to update.
            definition (dict): The updated definition of the Report.

        Returns:
            Report: The updated Report object.

        Reference:
        - [Update Report Definition](https://learn.microsoft.com/en-us/rest/api/fabric/report/items/update-report-definition?tabs=HTTP)
        """

        body = {
            "displayName":"N/A",
            "definition":definition
        }
        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/reports/{report_id}/updateDefinition",
            auth=self._auth,
            item=Item(**body)
        )
        return resp
    
    def clone(self, source_workspace_id: uuid.UUID, report_id: uuid.UUID, clone_name: str, target_workspace_id: Optional[uuid.UUID]) -> Report:
        """
        Clone Report

        Clones a Report from the source workspace to the target workspace.

        Args:
            source_workspace_id (uuid.UUID): The ID of the source workspace.
            report_id (uuid.UUID): The ID of the Report to clone.
            clone_name (str): The name of the cloned Report.
            target_workspace_id (uuid.UUID, optional): The ID of the target workspace. If not provided, the Report is cloned to the source workspace. Defaults to None.

        Returns:
            Report: The cloned Report.

        """
        source_report = self.get(source_workspace_id, report_id, include_defintion=True)
        if target_workspace_id is None:
            target_workspace_id = source_workspace_id
        cloned_rpt =  self.create(target_workspace_id, display_name=clone_name, definition=source_report.definition, description=source_report.description)
        return cloned_rpt


