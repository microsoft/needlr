import pytest
from needlr.utils.util import FabricException

from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.notebook import Notebook

from needlr.models.jobscheduler import (ItemSchedules 
)

class TestWorkspaceJobScheduler:

    # we need an item to work with
    def test_notebook_ls(self, fc: FabricClient, workspace_test: Workspace, notebook_test:Notebook):
        int_nb = notebook_test
        notebooks = fc.notebook.ls(workspace_id=workspace_test.id)
        assert len(list(notebooks)) > 0    

    

    def test_list_item_schedules(self, fc: FabricClient, workspace_test: Workspace):
        pass


