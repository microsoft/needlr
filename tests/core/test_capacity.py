from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.item import ItemType
from needlr.models.capacity import Capacity
from needlr.models.git import GitStatusResponse

class TestCapacityLifeCycle:


    def test_workspace_capacity_ls(self, fc: FabricClient, workspace_test: Workspace):
        capacities = fc.capacity.list_capacities()
        assert len(list(capacities)) >= 0
