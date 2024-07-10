from .core.workspace.workspace import _WorkspaceClient
from .admin.workspace.adminworkspace import _AdminWorkspaceClient
from needlr.datawarehouse.warehouse.mirroredwarehouse import _MirroredWarehouseClient
from needlr.datawarehouse.warehouse.warehouse import _WarehouseClient




class FabricClient():
    def __init__(self, auth, **kwargs):
        self._auth = auth
        self._base_url = kwargs.get("base_url") if "base_url" in kwargs else "https://api.fabric.microsoft.com/v1/"
        self.workspace = _WorkspaceClient(auth=auth, base_url=self._base_url)
        self.admin_workspace = _AdminWorkspaceClient(auth=auth, base_url=self._base_url)
        self.warehouse = _WarehouseClient(auth=auth, base_url=self._base_url)
        self.mirroredwarehouse = _MirroredWarehouseClient(auth=auth, base_url=self._base_url)
        
        
    