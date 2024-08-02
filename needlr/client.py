from .core.workspace.workspace import _WorkspaceClient
from .admin.workspace.adminworkspace import _AdminWorkspaceClient
from needlr.datawarehouse.warehouse.mirroredwarehouse import _MirroredWarehouseClient
from needlr.datawarehouse.warehouse.warehouse import _WarehouseClient
from needlr.powerbi.semanticmodel import _SemanticModelClient
from needlr.powerbi.dashboard import _DashboardClient
from needlr.powerbi.datamart import _DatamartClient
from needlr.powerbi.paginatedreport import _PaginatedReportClient
from needlr.dataengineering.sqlendpoints import _SQLEndpointClient
from needlr.powerbi.report import _ReportClient 



class FabricClient():
    def __init__(self, auth, **kwargs):
        self._auth = auth
        self._base_url = kwargs.get("base_url") if "base_url" in kwargs else "https://api.fabric.microsoft.com/v1/"
        self.workspace = _WorkspaceClient(auth=auth, base_url=self._base_url)
        self.admin_workspace = _AdminWorkspaceClient(auth=auth, base_url=self._base_url)
        self.warehouse = _WarehouseClient(auth=auth, base_url=self._base_url)
        self.mirroredwarehouse = _MirroredWarehouseClient(auth=auth, base_url=self._base_url)
        self.semanticmodel = _SemanticModelClient(auth=auth, base_url=self._base_url)
        self.dashboardclient = _DashboardClient(auth=auth, base_url=self._base_url)
        self.datamartclient = _DatamartClient(auth=auth, base_url=self._base_url)
        self.paginatedreportclient = _PaginatedReportClient(auth=auth, base_url=self._base_url)
        self.sqlendpoint = _SQLEndpointClient(auth=auth, base_url=self._base_url)
        self.report = _ReportClient(auth=auth, base_url=self._base_url)
        
    