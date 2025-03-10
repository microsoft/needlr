from needlr import FabricClient
from needlr.models.item import Item, ItemType
from needlr import FabricClient

class TestUser:

    def test_user_access(self, fc: FabricClient, testParameters: dict):
        uacc = fc.user.access(
            userId=testParameters['fabric_admin_upn'],
            # itemType=ItemType.Report
        )
        uaccl = list(uacc) 
        assert len(list(uaccl)) > 0