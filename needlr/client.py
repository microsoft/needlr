
from needlr.core.workspace.workspace import _WorkspaceClient
from needlr.admin.workspace.adminworkspace import _AdminWorkspaceClient
from needlr.admin.tenant import _TenantClient
from needlr.core.capacity import _CapacityClient
from needlr.dataengineering.notebook import _NotebookClient
from needlr.dataengineering.sqlendpoints import _SQLEndpointClient
from needlr.datafactory.datapipeline import _DatapipelineClient
from needlr.datawarehouse.mirroredwarehouse import _MirroredWarehouseClient
from needlr.datawarehouse.warehouse import _WarehouseClient
from needlr.dataengineering.lakehouse import _LakehouseClient
from needlr.powerbi.dashboard import _DashboardClient
from needlr.powerbi.datamart import _DatamartClient
from needlr.powerbi.paginatedreport import _PaginatedReportClient
from needlr.powerbi.report import _ReportClient
from needlr.powerbi.semanticmodel import _SemanticModelClient
from needlr.realtimeintelligence.eventhouse import _EventhouseClient
from needlr.realtimeintelligence.eventstream import _EvenstreamClient
from needlr.realtimeintelligence.kqldatabase import _KQLDatabaseClient
from needlr.realtimeintelligence.kqlqueryset import _KQLQuerySetClient
from needlr.admin.domain import _DomainClient
from needlr.datascience.mlmodel import _MLModelClient
from needlr.datascience.mlexperiment import _MLExperimentClient
from needlr.dataactivator.reflex.reflex import _ReflexClient
from needlr.realtimeintelligence.kqldashboard import _KQLDashboardClient




class FabricClient():
    def __init__(self, auth, **kwargs):
        self._auth = auth
        self._base_url = kwargs.get("base_url") if "base_url" in kwargs else "https://api.fabric.microsoft.com/v1/"
        self.workspace = _WorkspaceClient(auth=auth, base_url=self._base_url)
        self.capacity = _CapacityClient(auth=auth, base_url=self._base_url)
        self.admin_workspaceclient = _AdminWorkspaceClient(auth=auth, base_url=self._base_url)
        self.warehouse = _WarehouseClient(auth=auth, base_url=self._base_url)
        self.lakehouse = _LakehouseClient(auth=auth, base_url=self._base_url)
        self.mirroredwarehouse = _MirroredWarehouseClient(auth=auth, base_url=self._base_url)
        self.semanticmodel = _SemanticModelClient(auth=auth, base_url=self._base_url)
        self.dashboardclient = _DashboardClient(auth=auth, base_url=self._base_url)
        self.datamartclient = _DatamartClient(auth=auth, base_url=self._base_url)
        self.paginatedreportclient = _PaginatedReportClient(auth=auth, base_url=self._base_url)
        self.sqlendpoint = _SQLEndpointClient(auth=auth, base_url=self._base_url)
        self.report = _ReportClient(auth=auth, base_url=self._base_url)
        self.eventhouse = _EventhouseClient(auth=auth, base_url=self._base_url)
        self.eventstream = _EvenstreamClient(auth=auth, base_url=self._base_url)
        self.kqldatabase = _KQLDatabaseClient(auth=auth, base_url=self._base_url)
        self.kqlqueryset = _KQLQuerySetClient(auth=auth, base_url=self._base_url)
        self.datapipeline = _DatapipelineClient(auth=auth, base_url=self._base_url)
        self.notebook = _NotebookClient(auth=auth, base_url=self._base_url)
        self.tenant = _TenantClient(auth=auth, base_url=self._base_url)
        self.domain = _DomainClient(auth=auth, base_url=self._base_url)
        self.mlmodel = _MLModelClient(auth=auth, base_url=self._base_url)
        self.mlexperiment = _MLExperimentClient(auth=auth, base_url=self._base_url)
        self.reflex = _ReflexClient(auth=auth, base_url=self._base_url)
        self.kqldashboard = _KQLDashboardClient(auth=auth, base_url=self._base_url)

