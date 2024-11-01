import pytest

from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.tenant import TenantSetting

class TestTenant:

    def test_lts(self, fc: FabricClient):
        resp = fc.tenant.lts()
        assert len(list(resp)) > 0


    def test_list_capacities_tenant_settings_overrides(self, fc: FabricClient):
        resp = fc.tenant.list_capacities_tenant_settings_overrides()
        assert len(list(resp)) > 0