from typing import Optional
import base64
from needlr import auth, FabricClient
from needlr.models.item import Item, ItemType
from needlr.core.workspace.role import GroupPrincipal, WorkspaceRole
import pickle

fr = FabricClient(auth=auth.FabricInteractiveAuth(scopes=['https://api.fabric.microsoft.com/.default'])
                )

dev_ws_id = "63549f4b-bf02-430e-8773-0c9dbbfabf9d"
a = fr.report.ls(workspace_id=dev_ws_id)
for i in a:
    print(i)
    a2 = fr.report.get(workspace_id=dev_ws_id,
                       report_id=str(i.id), include_defintion=True)
    a30 = base64.b64decode(a2.definition['parts'][0]['payload'])
    # a31 = base64.b64decode(a2.definition['parts'][1]['payload'])
    # a32 = base64.b64decode(a2.definition['parts'][2]['payload'])
    # a33 = base64.b64decode(a2.definition['parts'][3]['payload'])
    pickle.dump(a2.definition, open('../tests/powerbi/report_definition.pkl', 'wb'))
    print("Stop here")


with open('../tests/powerbi/semantic_model_definition.pkl', 'rb') as sample_semantic_model_definition:
    definition = pickle.load(sample_semantic_model_definition)
    a = definition
   
    a30 = base64.b64decode(definition['parts'][0]['payload'])
    a31 = base64.b64decode(definition['parts'][1]['payload'])
    a32 = base64.b64decode(definition['parts'][2]['payload'])
    a33 = base64.b64decode(definition['parts'][3]['payload'])
    a34 = base64.b64decode(definition['parts'][4]['payload'])
    a35 = base64.b64decode(definition['parts'][5]['payload'])
    
    a = definition    

with open('../tests/powerbi/report_definition.pkl', 'rb') as sample_report_definition:
    definition = pickle.load(sample_report_definition)
    a = definition
    a30 = base64.b64decode(definition['parts'][0]['payload'])
    a31 = base64.b64decode(definition['parts'][1]['payload'])
    a32 = base64.b64decode(definition['parts'][2]['payload'])
    a = definition

# ws = fr.workspace.create(display_name=wsname, capacity_id='558B0068-C465-4249-895E-A3985CBE841C', description='test')


# sms = fr.semanticmodel.ls(workspace_id="8f948b27-4a22-491e-b56a-40d48aa58dd4")
# for sm in sms:
#     a2 = fr.semanticmodel.get(workspace_id="8f948b27-4a22-491e-b56a-40d48aa58dd4", 
#                               semanticmodel_id=sm.id, include_defintion=True)
#     pickle.dump(a2.definition, open('../tests/powerbi/semantic_model_definition.pkl', 'wb'))

dev_ws_id = "e951d4bf-eb6b-4973-8b38-560d91ba57db"
a = fr.report.ls(workspace_id=dev_ws_id)
for i in a:
    print(i)
    a2 = fr.report.get(workspace_id=dev_ws_id,
                       report_id=str(i.id), include_defintion=True)
    a30 = base64.b64decode(a2.definition['parts'][0]['payload'])
    a31 = base64.b64decode(a2.definition['parts'][1]['payload'])
    a32 = base64.b64decode(a2.definition['parts'][2]['payload'])
    a33 = base64.b64decode(a2.definition['parts'][3]['payload'])
    #pickle.dump(a2.definition, open('../tests/powerbi/report_definition.pkl', 'wb'))
    print("Stop here")
print("Stop here")
# print(fr.workspace.ls())
# for _ in fr.workspace.ls():
#     print(_)


# print(fr.workspace.item_ls(workspace_id='9bbbcb66-a075-407e-b0a7-9052ed2840d0'))
# for _ in fr.workspace.item_ls(workspace_id='9bbbcb66-a075-407e-b0a7-9052ed2840d0'):
#     print(_)


# for _ in fr.admin_workspace.ls():
#     print(_)

# print(fr.admin_workspace.get(workspace_id='5bd603ee-cfa8-48e3-8f7e-ceb3dc6dbfd5'))

# sh = logging.StreamHandler()
# logger_faburest = logging.getLogger('needlr')
# logger_faburest.setLevel(logging.DEBUG)
# logger_faburest.addHandler(sh)

# print(fr.admin_workspace.item_ls())
# print(len([_ for _ in fr.admin_workspace.item_ls()]))
# for i, _ in enumerate(fr.admin_workspace.item_ls()):
#     print(i, _)


# for _ in fr.admin_workspace.item_ls():
#     print(_)

#for _ in fr.workspace.item_ls(workspace_id='558B0068-C465-4249-895E-A3985CBE841C', type='Lakehouse'):
#    print(_)

wsname = 'TONIO_WS_TEST_1'
mirrored_ws_id ="27018a3b-d0ad-4925-9757-b09132484480"
semantic_model_ws_id = "e951d4bf-eb6b-4973-8b38-560d91ba57db"
semantic_model_to_delete_id = "d3735118-8aa6-4a76-8033-ea37966e0879"
sample_ws_id = "75609229-8f61-41f5-8b35-69a9e6188935"

# sms = fr.semanticmodel.ls(workspace_id=sample_ws_id)
# for sm in sms:
#     with open('../tests/powerbi/semantic_model_definition.pkl', 'rb') as sample_semantic_model_definition:
#             definition = pickle.load(sample_semantic_model_definition)
#             nsm = fr.semanticmodel.create(workspace_id=sample_ws_id, definition=definition, display_name='New_Sales2')
#             print(type(nsm))



# ws = fr.workspace.create(display_name=wsname, capacity_id='558B0068-C465-4249-895E-A3985CBE841C', description='test')
# a = fr.eventstream.create(workspace_id=sample_ws_id, display_name='eventstream1', description='eventstream1')
# b = a
# rpts = fr.report.ls(workspace_id=sample_ws_id)
# for rpt in rpts:
#     #r = fr.report.get(workspace_id=sample_ws_id, report_id='c177ec3f-c011-4096-94a2-193cbb4ea5e8/b562f9c8ce86df85cc37')
#     cloned_rpt = fr.report.clone(source_workspace_id=rpt.workspaceId, 
#                                  report_id=rpt.id, 
#                                  clone_name='cloned_'+rpt.name, 
#                                  target_workspace_id=ws.id)
#     a = cloned_rpt.id

# e = fr.eventhouse.create(workspace_id=ws.id, display_name='eventhouse1', description='eventhouse1')

# newkqlqs = fr.kqlqueryset.create(workspace_id='e6252f4b-3b44-4080-96d0-9b7a53883e09', display_name='kqlqs111', description='kqlqs111')

# kqlqs = fr.kqlqueryset.ls('e6252f4b-3b44-4080-96d0-9b7a53883e09')
# for kqlq in kqlqs:
#     a= kqlq
#     print(kqlq)



# kqldb = fr.kqldatabase.create_readwrite_database(workspace_id='e6252f4b-3b44-4080-96d0-9b7a53883e09', 
#                                                  parentEventhouseItem_id='2ea83110-0dde-4e73-94d2-95a738ca5f53', 
#                                                  display_name='kql_db8', 
#                                                  description='kql_db8') 
# a = kqldb.id
# b = fr.kqldatabase.get(workspace_id='e6252f4b-3b44-4080-96d0-9b7a53883e09', kqlDatabase_id=a)
# c= b
elh = fr.eventhouse.ls(workspace_id=sample_ws_id)
for e in elh: 
    ed = fr.eventhouse.get(workspace_id=sample_ws_id, eventhouse_id=e.id)
    cloned_e = fr.eventhouse.clone(source_workspace_id=ed.workspaceId, 
                                   eventhouse_id=ed.id, 
                                   clone_name='clone2_'+ed.name, 
                                   target_workspace_id=sample_ws_id)
    a = cloned_e.id

# wh = fr.warehouse.create(display_name='wh1', workspace_id=ws.id, description='wh1')
# print(wh)
# print(type(wh))

# sqlep = fr.sqlendpoint.ls(workspace_id="3b2191b6-9fe9-4fc8-8939-f069976d0aee")
# for s in sqlep:
#     b= s
#     print(s)

# pgl = fr.paginatedreportclient.ls(workspace_id=ws.id)
# for p in pgl:
#     print(p)

# dbs = fr.dashboardclient.ls(workspace_id=ws.id)
# for d in dbs:
#     print(d)

# a = fr.report.ls(workspace_id=sample_ws_id)
# for i in a:
#     print(i)
#     a2 = fr.report.get(workspace_id=sample_ws_id, report_id=str(i.id), include_defintion=True)
#     a4 = fr.report.clone(workspace_id=sample_ws_id, report_id=str(i.id), clone_name='cloned_'+i.name)
#     a5 = fr.report.update_definition(workspace_id=sample_ws_id, report_id=a4.id, definition=a2.definition)
#     a = a5

# a = fr.report.ls(workspace_id=sample_ws_id)
# for i in a:
#     print(i)
#     a2 = fr.report.get(workspace_id=sample_ws_id, report_id=str(i.id), include_defintion=True)
#     pickle.dump(a2.definition, open('../tests/powerbi/report_definition.pkl', 'wb'))

# r = fr.semanticmodel.delete(workspace_id=semantic_model_ws_id, semanticmodel_id=semantic_model_to_delete_id)
# print(r.is_successful)

# a = fr.semanticmodel.ls(workspace_id=semantic_model_ws_id)
# print(type(a))
# for i in a:
#     a2 = fr.semanticmodel.get(workspace_id=semantic_model_ws_id, semanticmodel_id=i.id, include_defintion=True)
#     with open('../tests/powerbi/semantic_model_definition.pkl', 'rb') as f:
#         a2.definition = pickle.load(f)
#     a3 = fr.semanticmodel.create(workspace_id=semantic_model_ws_id, display_name='New_Sales2', definition=a2.definition, description='test')
#     resp = fr.semanticmodel.update_definition(workspace_id=semantic_model_ws_id, semanticmodel_id=a3.id, definition=a3.definition)
#     a3 = fr.semanticmodel.get_definition(workspace_id=semantic_model_ws_id, semanticmodel_id=i.id) 
#     break

#pr = GroupPrincipal(id="d93322d5-ba1e-4af6-8778-784c0944dd8b")
#print(pr)

#ws = fr.workspace.create(display_name=wsname, capacity_id='558B0068-C465-4249-895E-A3985CBE841C', description='test')
#print(ws)
#print(type(ws))

#res = fr.workspace.role.assign(workspace_id=ws.id, principal=GroupPrincipal(id="d93322d5-ba1e-4af6-8778-784c0944dd8b"), role=WorkspaceRole.Contributor)
#print(res.is_successful)

#res = fr.workspace.role.ls(workspace_id=ws.id)
#print(list(res))

#res = fr.workspace.role.update(workspace_id=ws.id, principal=GroupPrincipal(id="d93322d5-ba1e-4af6-8778-784c0944dd8b"), role=WorkspaceRole.Member)
#print(res.is_successful)

#res = fr.workspace.role.delete(workspace_id=ws.id, principal=GroupPrincipal(id="d93322d5-ba1e-4af6-8778-784c0944dd8b"))
#print(res.is_successful)


#wh = fr.warehouse.create(display_name='wh1', workspace_id=ws.id, description='wh1')
#print(wh)
#print(type(wh))



"""
ws2 = fr.workspace.update(workspace_id=ws.id, display_name='New'+wsname)
print(ws2)
print(type(ws2))

print(((ws for ws in fr.workspace.ls() if ws.name == 'New'+wsname).__next__()).name)

print("Before unassign")
print(fr.workspace.get(workspace_id=ws.id))

a = fr.workspace.capacity_unassign(workspace_id=ws.id)

print("After  unassign")
print(fr.workspace.get(workspace_id=ws.id))

print("After  re-assign")
a = fr.workspace.capacity_assign(workspace_id=ws.id, capacity_id='558B0068-C465-4249-895E-A3985CBE841C')
print(fr.workspace.get(workspace_id=ws.id))

for il in fr.workspace.item_ls(workspace_id=ws.id):
    print(il)

for il in fr.workspace.item_ls(workspace_id="e951d4bf-eb6b-4973-8b38-560d91ba57db", item_type=ItemType.DataPipeline):
    print(il)


print((fr.workspace.delete(workspace_id=ws.id)).is_successful)
"""