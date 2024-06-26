from .core.workspace import _WorkspaceClient
from .admin.workspace import _AdminWorkspaceClient
# from .admin.item import WarehouseItem, LakehouseItem, FabricItem


class FabricClient():
    def __init__(self, auth, **kwargs):
        self._auth = auth
        self._base_url = kwargs.get("base_url") if "base_url" in kwargs else "https://api.fabric.microsoft.com/v1/"
        self.workspace = _WorkspaceClient(auth=auth, base_url=self._base_url)
        self.admin_workspace = _AdminWorkspaceClient(auth=auth, base_url=self._base_url)
        # self.admin_item = FabricItem(auth=auth, base_url=self._base_url)
        
    