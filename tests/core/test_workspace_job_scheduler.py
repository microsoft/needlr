import pytest
from needlr.utils.util import FabricException

from needlr import FabricClient
from needlr.models.workspace import Workspace

from needlr.models.jobscheduler import (ItemSchedules 
)

class TestWorkspaceJobScheduler:

    def test_list_item_schedules(self, fc: FabricClient, workspace_test: Workspace):
        pass


