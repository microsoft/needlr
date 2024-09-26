"""Module providing Core Datamart functions."""

from collections.abc import Iterator
import uuid

from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.paginatedreport import PaginatedReport
from needlr.models.item import Item


class _PaginatedReportClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/paginatedreport/items)

    ### Coverage

    * Update Paginated Report Definition > update_definition()
    * List Paginated Report > ls()
    * Update Paginated Report definition > update_definition()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a Paginated Report.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL for the Paginated Report.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def ls(self, workspace_id:uuid.UUID) -> Iterator[PaginatedReport]:
            """
            List PaginatedReport

            Retrieves a list of Paginated Reports associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.

            Yields:
                Iterator[PaginatedReport]: An iterator of Paginate dReport objects.

            Reference:
                [List PaginatedReport](GET https://learn.microsoft.com/en-us/rest/api/fabric/paginatedreport/items/list-paginated-reports?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/paginatedReports",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield PaginatedReport(**item)

    def update_definition(self, workspace_id:uuid.UUID, paginatedReport_id:uuid.UUID, display_name:str, description:str) -> PaginatedReport:
        """
        Update Paginated Report Definition

        This method updates the definition of a Paginated Report in Power BI.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the Paginated Report is located.
            paginatedReport_id (uuid.UUID): The ID of the Paginated Report to update.
            definition (dict): The updated definition of the Paginated Report.

        Returns:
            PaginatedReport: The updated paginated report object.

        Reference:
        - [Update Paginated Report Definition]PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/paginatedReports/{paginatedReportId})
        """
        body = dict()
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/paginatedReports/{paginatedReport_id}/updateDefinition",
            auth=self._auth,
            item=Item(**body)
        )
        return resp
