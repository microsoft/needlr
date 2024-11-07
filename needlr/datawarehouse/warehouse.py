"""Module providing Core Warehouse functions."""

from collections.abc import Iterator
import uuid
import itertools
import struct
import pyodbc
from needlr import auth

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.warehouse import Warehouse



class _WarehouseClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items)

    ### Coverage

    * Create Warehouse > create()
    * Delete Warehouse > delete()
    * Get Warehouse > get()
    * List Warehouses > ls()
    * Update Warehouse > update()
    * Submit SQL Query > submit_sql_query()
    * Check V-Order > check_v_order()
    * Disable V-Order > disable_v_order()


    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a Warehouse object.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the warehouse.

        """        
        self._auth = auth
        self._base_url = base_url

    def create(self, display_name:str, workspace_id:uuid.UUID, description:str=None) -> Warehouse:
        """
        Create Warehouse

        This method creates a new warehouse in the data warehouse system.

        Args:
            display_name (str): The display name of the warehouse.
            workspace_id (uuid.UUID): The ID of the workspace where the warehouse will be created.
            description (str, optional): The description of the warehouse. Defaults to None.

        Returns:
            Warehouse: The created warehouse object.

        Reference:
        - [Create Warehouse](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/create-warehouse?tabs=HTTP)
        """
        body = {
            "displayName":display_name
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses",
            auth=self._auth,
            item=Warehouse(**body)
        )
        return Warehouse(**resp.body)

    def delete(self, workspace_id:uuid.UUID, warehouse_id:uuid.UUID) -> FabricResponse:
        """
        Delete Warehouse

        Deletes a warehouse with the specified `warehouse_id` in the given `workspace_id`.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            warehouse_id (uuid.UUID): The ID of the warehouse to be deleted.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
        - [Delete Warehouse](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/delete-warehouse?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses/{warehouse_id}",
            auth=self._auth
        )
        return resp
    
    def get(self, workspace_id:uuid.UUID, warehouse_id:uuid.UUID) -> Warehouse:
        """
        Get Warehouses

        Retrieves a specific warehouse from the data warehouse.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            warehouse_id (uuid.UUID): The ID of the warehouse.

        Returns:
            Warehouse: The retrieved warehouse object.

        Reference:
        [Microsoft Documentation](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/get-warehouse?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses/{warehouse_id}",
            auth=self._auth
        )
        warehouse = Warehouse(**resp.body)
        return warehouse

    def ls(self, workspace_id:uuid.UUID) -> Iterator[Warehouse]:
        """
        List Warehouses

        This method retrieves a list of warehouses associated with the specified workspace ID.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.

        Returns:
            Iterator[Warehouse]: An iterator that yields Warehouse objects.

        Reference:
        - [List Warehouses](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/list-warehouses?tabs=HTTP)
        """
        resp = _http._get_http_paged(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses",
            auth=self._auth,
            items_extract=lambda x:x["value"]
        )
        for page in resp:
            for item in page.items:
                yield Warehouse(**item)

    def update(self, workspace_id:uuid.UUID, warehouse_id:uuid.UUID, display_name:str=None, description:str=None) -> Warehouse:
        """
        Updates the properties of the specified warehouse

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the warehouse.
            warehouse_id (uuid.UUID): The ID of the warehouse to update.
            display_name (str, optional): The new display name for the warehouse.
            description (str, optional): The new description for the warehouse.

        Returns:
            Warehouse: The updated warehouse object.

        Raises:
            ValueError: If both `display_name` and `description` are left blank.

        Reference:
            [Microsoft Docs](https://learn.microsoft.com/en-us/rest/api/fabric/warehouse/items/update-warehouse?tabs=HTTP)
        """
        if ((display_name is None) and (description is None)):
            raise ValueError("display_name or description must be provided")

        body = dict()
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/warehouses/{warehouse_id}",
            auth=self._auth,
            json=body
        )
        warehouse = Warehouse(**resp.body)
        return warehouse

    def submit_sql_query(self, workspace_id:uuid.UUID, warehouse_id:uuid.UUID, query:str):
        """
        Submit SQL Query

        This method submits a SQL query to the specified warehouse.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            warehouse_id (uuid.UUID): The ID of the warehouse.
            query (str): The SQL query to be executed.

        Returns:
            FabricResponse: The response from the query submission.
        """
        warehouse = self.get(workspace_id, warehouse_id)
        warehouse_name = warehouse.name
        server = warehouse.properties.get('connectionString','')
        connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};Database={warehouse_name}'
        #TODO: Temporary workaround until Auth supports multiple scopes
        fr2 = auth.FabricInteractiveAuth(scopes=['https://analysis.windows.net/powerbi/api/.default'])
        #token = bytes(self._auth._get_token(), "UTF-8") # Convert the token to a UTF-8 byte string
        #token = bytes(fr2._auth._get_token(), "UTF-8")
        token = bytes(fr2._get_token(), "UTF-8")
        encoded_bytes = bytes(itertools.chain.from_iterable(zip(token, itertools.repeat(0)))) # Encode the bytes to a Windows byte string
        token_struct = struct.pack("<i", len(encoded_bytes)) + encoded_bytes # Package the token into a bytes object

        def get_result_set(cursor):
            if cursor.description:
                resultList = cursor.fetchall()
                resultColumns = [column[0] for column in cursor.description]
            else:
                resultList = []
                resultColumns = []
            return [dict(zip(resultColumns, [str(col) for col in row])) for row in resultList]
        
        with pyodbc.connect(connection_string, autocommit=True, attrs_before = {1256:token_struct}) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result_set = get_result_set(cursor)
        return result_set

    def check_v_order(self, workspace_id:uuid.UUID, warehouse_id:uuid.UUID) -> bool:
        """
        Check Status of v-Order on Warehouse

        This method checks the statusn of v-ordfer (on or off) on the warehouse.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            warehouse_id (uuid.UUID): The ID of the warehouse.

        Returns:
            V-Order Enabled: True if v-order is enabled on Warehouse, False otherwise. None if the Warehouse Id does not exist

        Reference:
        - [Check if Warehouse V-Order is enabled]()
        """
        warehouse_name = self.get(workspace_id, warehouse_id).name
        query = f"SELECT is_vorder_enabled FROM sys.databases WHERE name = '{warehouse_name}';"
        res = self.submit_sql_query(workspace_id, warehouse_id, query)
        if len(res) == 1:
            return res[0]["is_vorder_enabled"]
        else:
            return None
    
    def disable_v_order(self, workspace_id:uuid.UUID, warehouse_id:uuid.UUID) -> bool:
        """
        Disable V-Order on Warehouse

        This method disables v-order on the specified warehouse.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            warehouse_id (uuid.UUID): The ID of the warehouse.

        Returns:
            bool: True if v-order was successfully disabled, False otherwise.

        Reference:
        - [Disable V-Order on Warehouse]()
        """
        warehouse_name = self.get(workspace_id, warehouse_id).name
        query = f"ALTER DATABASE {warehouse_name} SET VORDER = OFF"
        self.submit_sql_query(workspace_id, warehouse_id, query)
        # Check if change was applied
        return not self.check_v_order(workspace_id, warehouse_id) # True if v-order is now disabled, False otherwise
