import csv

from needlr import auth, FabricClient
from needlr.models.workspace import Workspace

fc = FabricClient(auth=auth.FabricInteractiveAuth(scopes=['https://api.fabric.microsoft.com/.default']))

with open('project.csv', mode='r', encoding='utf-8') as file:
    for row in csv.DictReader(file):
        template_ws: Workspace = fc.workspace.get('DataScienceTemplate')
        ws = fc.workspace.create(display_name=row['Workspace_Name'],capacity_id=template_ws.capacityId)
        fc.lakehouse.create(display_name=row['Lakehouse_Name'],workspace_id=ws.id)
        fc.notebook.create(display_name=row['Notebook_Name'],workspace_id=ws.id)
#
        fc.warehouse.create(display_name=row['Warehouse_Name'],workspace_id=ws.id)
#
        fc.semanticmodel.clone(source_workspace_id=template_ws.id, 
                                    semanticmodel_id=list(fc.semanticmodel.ls(workspace_id=template_ws.id))[0].id,
                                    clone_name='AnalyticsProjectSemanticModel', target_workspace_id=ws.id)
        fc.report.clone(source_workspace_id=template_ws.id,
                             report_id=list(fc.report.ls(workspace_id=template_ws.id))[0].id,
                             clone_name='AnalyticsProjectReport', target_workspace_id=ws.id)
#
        fc.workspace.capacity_assign(ws.id, capacity_id=fc.workspace.get('LargeDataScienceWS').capacityId)
        fc.workspace.role.assign(ws.id, principal=row['DS_GUID'], role='Contributor')
#
        fc.workspace.git_connect(ws.id, organization_Name='Data Science Repo', project='DS Project', gitProviderType='AzureDevOps', 
                                 repository='DS Repo', branch='main')
