from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.lakehouse import Lakehouse
import time
import pytest
from azure.storage.filedatalake import (
    DataLakeServiceClient
)
from azure.identity import DefaultAzureCredential

class TestLakehouseLifeCycle:

    def test_lakehouse_ls(self, fc: FabricClient, workspace_test: Workspace, lakehouse_test: Lakehouse):
        lhl = fc.lakehouse.ls(workspace_id=workspace_test.id)
        assert len(lhl) == 1

    def test_lakehouse_get(self, fc: FabricClient, workspace_test: Workspace, lakehouse_test: Lakehouse):
        lh = fc.lakehouse.get(workspace_id=workspace_test.id, lakehouse_id=lakehouse_test.id)
        assert lh.id == lakehouse_test.id

    def test_lakehouse_update(self, fc: FabricClient, workspace_test: Workspace, lakehouse_test: Lakehouse, testParameters: dict[str, str]):
        # Make sure it is fully provisioned before trying to update
        lh = fc.lakehouse.get(workspace_id=workspace_test.id, lakehouse_id=lakehouse_test.id)
        while lh.properties['sqlEndpointProperties']['provisioningStatus'] == 'InProgress':
            time.sleep(5)
            lh = fc.lakehouse.get(workspace_id=workspace_test.id, lakehouse_id=lakehouse_test.id)
        lh = fc.lakehouse.update(workspace_id=workspace_test.id, lakehouse_id=lakehouse_test.id, display_name='new'+testParameters['lakehouse_name'])
        lh = fc.lakehouse.get(workspace_id=workspace_test.id, lakehouse_id=lakehouse_test.id)
        assert lh.displayName == 'new'+testParameters['lakehouse_name']

    def test_lakehouse_list_tables(self, fc: FabricClient, workspace_test: Workspace, lakehouse_test: Lakehouse):
        table_list = fc.lakehouse.list_tables(workspace_id=workspace_test.id, lakehouse_id=lakehouse_test.id)
        assert len(table_list) == 0

    @pytest.mark.skip(reason="Requires loading a file first - Needs authentication")
    def test_lakehouse_load_table(self, fc: FabricClient, workspace_test: Workspace, lakehouse_test: Lakehouse):
        account_url = f"https://{workspace_test.name}.dfs.core.windows.net"
        token_credential = DefaultAzureCredential()
        service_client = DataLakeServiceClient(account_url, credential=token_credential)
        file_system_client = service_client.get_file_system_client(workspace_test.name)
        directory_client = file_system_client.get_directory_client("/Files")
        file_client = directory_client.create_file("dimension_customer.csv")    
        # Upload file
        with open('tests/dataengineering/dimension_customer.csv', 'rb') as data:
            file_client.upload_data(data, overwrite=True)
        # Create Table
        resp = fc.lakehouse.load_table(workspace_id=workspace_test.id, lakehouse_id=lakehouse_test.id, 
                                table_name='dimension_customer', relative_path='Files/dimension_customer.csv',
                                path_type='File', mode='Overwrite', recursive=False,
                                format='CSV', delimiter=',', header=True)
        assert resp is not None

    def test_run_table_maintenance(self, fc: FabricClient, workspace_test: Workspace, lakehouse_test: Lakehouse):
        resp = fc.lakehouse.run_table_maintenance(workspace_id=workspace_test.id, lakehouse_id=lakehouse_test.id, table_name='dimension_customer',
                schema_name='dbo', vOrder=True, zOrderBy=['CustomerKey', 'PostalCode'],
                vacuumSettings_retentionPeriod = "7:01:00:00")
        assert resp.is_successful

    def test_lakehouse_delete(self, fc: FabricClient, workspace_test: Workspace, lakehouse_test: Lakehouse):
        fc.lakehouse.delete(workspace_id=workspace_test.id, lakehouse_id=lakehouse_test.id)
        lhl = fc.lakehouse.ls(workspace_id=workspace_test.id)
        assert len(lhl) == 0