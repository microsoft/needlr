from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.report import Report
from needlr.models.datapipeline import Datapipeline

import uuid

class TestLabelLifeCycle:

    def test_label_bulk_remove(self, fc: FabricClient, workspace_test: Workspace):
        lh1 = fc.lakehouse.create(
            workspace_id=workspace_test.id,
            display_name='TestLakehouse1',
            description='Test Lakehouse Description'
        )
        lh2 = fc.lakehouse.create(
            workspace_id=workspace_test.id,
            display_name='TestLakehouse2',
            description='Test Lakehouse Description'
        )
        items = [
            {
                "id": str(lh1.id),
                "type": "Lakehouse"
            },
            {
                "id": str(lh2.id),
                "type": "Lakehouse"
            }
        ]
        resp = fc.label.bulk_remove(items)
        assert resp.status_code == 200

    def test_label_bulk_set(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
        lh1 = fc.lakehouse.create(
            workspace_id=workspace_test.id,
            display_name='TestLakehouse1',
            description='Test Lakehouse Description'
        )
        lh2 = fc.lakehouse.create(
            workspace_id=workspace_test.id,
            display_name='TestLakehouse2',
            description='Test Lakehouse Description'
        )
        item_list = [
            {
                "id": str(lh1.id),
                "type": "Lakehouse"
            },
            {
                "id": str(lh2.id),
                "type": "Lakehouse"
            }
        ]
        resp = fc.label.bulk_set(item_list=item_list, label_id=testParameters['label_general_id'])
        assert resp.status_code == 200