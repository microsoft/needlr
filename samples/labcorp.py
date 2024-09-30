""" 
    This script is a sample script that demonstrates how to 
    use the FabricClient to interact with the Fabric API.
"""

import pickle

from needlr import auth, FabricClient

#Some sample variables
wsname = 'TONIO_WS_TEST_1'
mirrored_ws_id ="27018a3b-d0ad-4925-9757-b09132484480"
semantic_model_ws_id = "e951d4bf-eb6b-4973-8b38-560d91ba57db"
semantic_model_to_delete_id = "d3735118-8aa6-4a76-8033-ea37966e0879"


# Fabric CLient with Interactive Auth
fr = FabricClient(auth=auth.FabricInteractiveAuth(scopes=['https://api.fabric.microsoft.com/.default']))

# Print WOrkspace List
for ws in fr.workspace.ls():
    print(ws.name)

# Create a new workspace
ws = fr.workspace.create(display_name=wsname, 
                         capacity_id='9828D8D8-27A1-4CC2-A227-F166FE35ABB8', 
                         description='test')
print(ws)

# Create a new Warehouse    
wh = fr.warehouse.create(workspace_id=ws.id, 
                         display_name='New_Warehouse', 
                         description='test')
print(wh)

# Create a new Semantic Model
with open('../tests/powerbi/semantic_model_definition.pkl', 'rb') as f:
    a3 = fr.semanticmodel.create(workspace_id=semantic_model_ws_id, 
                                 display_name='New_Sales2', 
                                 definition=pickle.load(f), 
                                 description='test')
    resp = fr.semanticmodel.update_definition(workspace_id=semantic_model_ws_id, 
                                              semanticmodel_id=a3.id, 
                                              definition=a3.definition)
    print(a3)
    fr.semanticmodel.delete(workspace_id=semantic_model_ws_id, 
                            semanticmodel_id=a3.id)

# Delete the Worksapce
resp = fr.workspace.delete(ws.id)