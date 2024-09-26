file: samples/ds.py
line: 1
---
import csv

from needlr import auth, FabricClient
from needlr.models.workspace import Workspace

fc = FabricClient(auth=auth.FabricInteractiveAuth(scopes=['https://api.fabric.microsoft.com/.default']))

with open('project.csv', mode='r') as file:
    for row in csv.DictReader(file):
        template_ws: Workspace = fc.workspace.get('DataScienceTemplate')
        ws = fc.workspace.create(display_name=row['Workspace_Name'],capacity_id=template_ws.capacityId)
        fc.lakehouse.create(display_name=row['Lakehouse_Name'],workspace_id=ws.id)
        fc.notebook.create(display_name=row['Notebook_Name'],workspace_id=ws.id)
