"""Module providing Lakehouse functions."""

from needlr.auth.auth import _FabricAuthentication

import uuid

from needlr.models.lakehouse import Lakehouse
from needlr.models.item import Item
from needlr import _http
from needlr._http import FabricResponse

from typing import Literal

class _LakehouseClient():
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/lakehouse/items)

    ### Coverage
    * Create a lakehouse > create
    * Delete a lakehouse > delete
    * List all lakehouses > list
    * Get a specific lakehouse > get
    * Update a lakehouse > update
    * List all tables in the lakehouse > list_tables
    * Load data into a table > load_table
    * Run on demand table maintenance > run_table_maintenance
    """

    TABLE_LOAD_PATH_TYPE = Literal["File", "Folder"]
    TABLE_LOAD_MODE = Literal["Append", "Overwrite"]
    TABLE_LOAD_FORMAT = Literal["Csv", "Parquet"]

    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a new instance of the Lakehouse class.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL of the Lakehouse.

        """
        self._auth = auth
        self._base_url = base_url

    def create(self, workspace_id:uuid.UUID, display_name:str, description:str=None, enableSchemas:bool=False) -> Lakehouse:
        """
        Creates a new lakehouse.

        Args:
            workspace_id (uuid.UUID): The workspace ID.
            display_name (str): The display name of the lakehouse.
            description (str): The description of the lakehouse.
            enableSchemas (bool): The enable schemas flag.

        Returns:
            lakehouse: The created lakehouse.

        Reference:
        [Create Lakehouse](https://learn.microsoft.com/en-us/rest/api/fabric/lakehouse/items/create-lakehouse?tabs=HTTP)
        """
        body = {
            "displayName":display_name
        }
        if description:
            body["description"] = description
        body["creationPayload"] = {
                "enableSchemas": enableSchemas
            }

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/lakehouses",
            auth=self._auth,
            item=Item(**body)
        )
        lakehouse = Lakehouse(**resp.body)
        return lakehouse

    def delete(self, workspace_id:uuid.UUID, lakehouse_id:uuid.UUID) -> FabricResponse:
        """
        Deletes a lakehouse.

        Args:
            workspace_id (uuid.UUID): The workspace ID.
            lakehouse_id (uuid.UUID): The lakehouse ID.

        Reference:
        [Delete Lakehouse](https://learn.microsoft.com/en-us/rest/api/fabric/lakehouse/items/delete-lakehouse?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/lakehouses/{lakehouse_id}",
            auth=self._auth
        )

        return resp

    def ls(self, workspace_id:uuid.UUID) -> list:
        """
        Lists all lakehouses.

        Args:
            workspace_id (uuid.UUID): The workspace ID.

        Returns:
            list: The list of lakehouses.

        Reference:
        [List Lakehouses](https://learn.microsoft.com/en-us/rest/api/fabric/lakehouse/items/list-lakehouses?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/lakehouses",
            auth=self._auth
        )
        return resp.body['value']

    def get(self, workspace_id:uuid.UUID, lakehouse_id:uuid.UUID) -> Lakehouse:
        """
        Gets a specific lakehouse.

        Args:
            workspace_id (uuid.UUID): The workspace ID.
            lakehouse_id (uuid.UUID): The lakehouse ID.

        Returns:
            lakehouse: The lakehouse.

        Reference:
        [Get Lakehouse](https://learn.microsoft.com/en-us/rest/api/fabric/lakehouse/items/get-lakehouse?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/lakehouses/{lakehouse_id}",
            auth=self._auth
        )
        lakehouse = Lakehouse(**resp.body)
        return lakehouse

    def update(self, workspace_id:uuid.UUID, lakehouse_id:uuid.UUID, display_name:str=None, description:str=None) -> Lakehouse:
        """
        Updates a lakehouse.

        Args:
            workspace_id (uuid.UUID): The workspace ID.
            lakehouse_id (uuid.UUID): The lakehouse ID.
            display_name (str): The display name of the lakehouse.
            description (str): The description of the lakehouse.

        Returns:
            lakehouse: The updated lakehouse.

        Reference:
        [Update Lakehouse](https://learn.microsoft.com/en-us/rest/api/fabric/lakehouse/items/update-lakehouse?tabs=HTTP)
        """
        body = {}
        if display_name:
            body["displayName"] = display_name
        if description:
            body["description"] = description

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/lakehouses/{lakehouse_id}",
            auth=self._auth,
            item=Item(**body)
        )
        lakehouse = Lakehouse(**resp.body)
        return lakehouse

    def list_tables(self, workspace_id:uuid.UUID, lakehouse_id:uuid.UUID) -> list:
        """
        Lists all tables in the lakehouse.

        Args:
            workspace_id (uuid.UUID): The workspace ID.
            lakehouse_id (uuid.UUID): The lakehouse ID.

        Returns:
            list: The list of tables.

        Reference:
        [List Tables](GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/tables)
        """
        resp = _http._get_http_paged(
            url = f"{self._base_url}workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables",
            auth=self._auth
        )
        return list(resp)[0].items

    def load_table(self, workspace_id:uuid.UUID, lakehouse_id:uuid.UUID, table_name:str, 
                    relative_path:str, path_type:TABLE_LOAD_PATH_TYPE = 'File', mode:TABLE_LOAD_MODE = 'Overwrite',
                    recursive:bool = False, format:TABLE_LOAD_FORMAT = 'Csv', header:bool = True, 
                    delimiter:str =',') -> FabricResponse:
        """
        Loads data into a table.

        Args:
            workspace_id (uuid.UUID): The workspace ID.
            lakehouse_id (uuid.UUID): The lakehouse ID.
            table_name (str): The table name.
            relative_path (str): The relative path.
            path_type (TABLE_LOAD_PATH_TYPE): The path type.
            mode (TABLE_LOAD_MODE): The mode.
            recursive (bool): The recursive flag.
            format (TABLE_LOAD_FORMAT): The format.
            header (bool): The header.
            delimiter (str): The delimiter.

        Returns:
            FabricResponse: The response.

        Reference:
        [Load Table](https://learn.microsoft.com/en-us/rest/api/fabric/lakehouse/items/load-table?tabs=HTTP)
        """
        body = {
                "relativePath": relative_path,
                "pathType": path_type,
                "mode": mode,
                "recursive": recursive,
                "formatOptions": {
                    "format": format
                }
            }
        if format == 'Csv':
            body.formatOptions = {
                    "header": header,
                    "delimiter": delimiter
                }
        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables/{table_name}/load",
            auth=self._auth,
            json_par=body
        )
        return resp

    def run_table_maintenance(self, workspace_id:uuid.UUID, lakehouse_id:uuid.UUID, table_name:str,
                             schema_name:str = None, vOrder:bool = None,
                             zOrderBy:list[str] = None, vacuumSettings_retentionPeriod:str = None) -> FabricResponse:
        """
        Runs on demand table maintenance.

        Args:
            workspace_id (uuid.UUID): The workspace ID.
            lakehouse_id (uuid.UUID): The lakehouse ID.
            table_name (str): The table name.
            schema_name (str): The schema name (Optional).
            vOrder (bool): The vOrder (Optional).
            zOrderBy (list[str]): A list of column names to Z-Order the data by. (Optional).
            vacuumSettings_retentionPeriod (str): Overrides the default retention period - d:hh:mm:ss (Optional).

        Returns:
            FabricResponse: The response.

        Reference:
        [Run Table Maintenance](https://learn.microsoft.com/en-us/rest/api/fabric/lakehouse/background-jobs/run-on-demand-table-maintenance?tabs=HTTP#vacuumsettings)
        """
        jobType = "TableMaintenance"
        params = {"executionData": {
                        "tableName": table_name,
                        "optimizeSettings": {}
                        }
                }
        if schema_name:
            params["executionData"]["schemaName"] = schema_name
        if vOrder:
            params["executionData"]["optimizeSettings"]["vOrder"] = vOrder
        if zOrderBy:
            params["executionData"]["optimizeSettings"]["zOrderBy"] = zOrderBy
        if vacuumSettings_retentionPeriod:
            params["executionData"]["optimizeSettings"]["vacuumSettings"] = {"retentionPeriod": vacuumSettings_retentionPeriod}
        resp = _http._post_http(
            url = f"{self._base_url}workspaces/{workspace_id}/lakehouses/{lakehouse_id}/jobs/instances?jobType={jobType}",
            auth=self._auth,
            json_par = params
        )
        return resp